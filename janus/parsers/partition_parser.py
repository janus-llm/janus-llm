import json
import random
import uuid

from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel, Field

from janus.language.block import CodeBlock
from janus.parsers.parser import JanusParser
from janus.utils.logger import create_logger

log = create_logger(__name__)
RNG = random.Random()


class PartitionObject(BaseModel):
    reasoning: str = Field(
        description="An explanation for why the code should be split at this point"
    )
    location: str = Field(
        description="The 8-character line label which should start a new chunk"
    )


class PartitionList(BaseModel):
    __root__: list[PartitionObject] = Field(
        description=(
            "A list of appropriate split points, each with a `reasoning` field "
            "that explains a justification for splitting the code at that point, "
            "and a `location` field which is simply the 8-character line ID. "
            "The `reasoning` field should always be included first."
        )
    )


class PartitionParser(JanusParser, PydanticOutputParser):
    token_limit: int
    model: BaseLanguageModel
    lines: list[str] = []
    line_id_to_index: dict[str, int] = {}

    def __init__(self, token_limit: int, model: BaseLanguageModel):
        PydanticOutputParser.__init__(
            self,
            pydantic_object=PartitionList,
            model=model,
            token_limit=token_limit,
        )

    def parse_input(self, block: CodeBlock) -> str:
        code = str(block.text)
        RNG.seed(code)

        self.lines = code.split("\n")

        # Generate a unique ID for each line (ensure they are unique)
        line_ids = set()
        while len(line_ids) < len(self.lines):
            line_ids.add(str(uuid.UUID(int=RNG.getrandbits(128), version=4))[:8])

        # Prepend each line with the corresponding ID, save the mapping
        self.line_id_to_index = {lid: i for i, lid in enumerate(line_ids)}
        processed = "\n".join(
            f"{line_id}\t{self.lines[i]}" for line_id, i in self.line_id_to_index.items()
        )
        return processed

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)

        try:
            out: PartitionList = super().parse(text)
        except (OutputParserException, json.JSONDecodeError):
            log.debug(f"Invalid JSON object. Output:\n{text}")
            raise

        # Locate any invalid line IDs, raise exception if any found
        invalid_splits = [
            partition.location
            for partition in out.__root__
            if partition.location not in self.line_id_to_index
        ]
        if invalid_splits:
            err_msg = (
                f"{len(invalid_splits)} line ID(s) not found in input: "
                + ", ".join(invalid_splits)
            )
            log.warning(err_msg)
            raise OutputParserException(err_msg)

        # Map line IDs to indices (so they can be sorted and lines indexed)
        index_to_line_id = {0: "START", None: "END"}
        split_points = {0}
        for partition in out.__root__:
            index = self.line_id_to_index[partition.location]
            index_to_line_id[index] = partition.location
            split_points.add(index)

        # Get partition start/ends, chunks, chunk lengths
        split_points = sorted(split_points) + [None]
        partition_indices = list(zip(split_points, split_points[1:]))
        partition_points = [
            (index_to_line_id[i0], index_to_line_id[i1]) for i0, i1 in partition_indices
        ]
        chunks = ["\n".join(self.lines[i0:i1]) for i0, i1 in partition_indices]
        chunk_tokens = list(map(self.model.get_num_tokens, chunks))

        # Collect any chunks that exceed token limit
        oversized_indices: list[int] = [
            i for i, n in enumerate(chunk_tokens) if n > self.token_limit
        ]
        if oversized_indices:
            data = list(zip(partition_points, chunks, chunk_tokens))
            data = [data[i] for i in oversized_indices]

            problem_points = "\n".join(
                [
                    f"{i0} to {i1} ({t / self.token_limit:.1f}x maximum length)"
                    for (i0, i1), _, t in data
                ]
            )
            log.warning(f"Found {len(data)} oversized chunks:\n{problem_points}")
            log.debug(
                "Oversized chunks:\n"
                + "\n#############\n".join(chunk for _, chunk, _ in data)
            )
            raise OutputParserException(
                f"The following segments are too long and must be "
                f"further subdivided:\n{problem_points}"
            )

        return "\n<JANUS_PARTITION>\n".join(chunks)
