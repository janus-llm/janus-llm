import json
import random
import uuid

from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel, Field

from janus.language.block import CodeBlock
from janus.parsers.parser import JanusParser, JanusParserException
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


# The following IDs appear in the prompt example. If the LLM produces them,
#  they should be ignored
EXAMPLE_IDS = {
    "0d2f4f8d",
    "def2a953",
    "75315253",
    "e7f928da",
    "1781b2a9",
    "2fe21e27",
    "9aef6179",
    "6061bd82",
    "22bd0c30",
    "5d85e19e",
    "06027969",
    "91b722fb",
    "4b3f79be",
    "k57w964a",
    "51638s96",
    "065o6q32",
    "j5q6p852",
}


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
            line_id = str(uuid.UUID(int=RNG.getrandbits(128), version=4))[:8]
            if line_id in EXAMPLE_IDS:
                continue
            line_ids.add(line_id)

        # Prepend each line with the corresponding ID, save the mapping
        self.line_id_to_index = {lid: i for i, lid in enumerate(line_ids)}
        processed = "\n".join(
            f"{line_id}\t{self.lines[i]}" for line_id, i in self.line_id_to_index.items()
        )
        return processed

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)
        original_text = text

        # Strip everything outside the JSON object
        begin, end = text.find("["), text.rfind("]")
        text = text[begin : end + 1]

        try:
            out: PartitionList = super().parse(text)
        except (OutputParserException, json.JSONDecodeError):
            log.debug(f"Invalid JSON object. Output:\n{text}")
            raise

        # Get partition locations, discard reasoning
        partition_locations = {partition.location for partition in out.__root__}

        # Ignore IDs from the example input
        partition_locations.difference_update(EXAMPLE_IDS)

        # Locate any invalid line IDs, raise exception if any found
        invalid_splits = partition_locations.difference(self.line_id_to_index)
        if invalid_splits:
            err_msg = (
                f"{len(invalid_splits)} line ID(s) not found in input: "
                + ", ".join(invalid_splits)
            )
            log.warning(err_msg)
            raise JanusParserException(original_text, err_msg)

        # Map line IDs to indices (so they can be sorted and lines indexed)
        index_to_line_id = {0: "START", None: "END"}
        split_points = {0}
        for partition in partition_locations:
            index = self.line_id_to_index[partition]
            index_to_line_id[index] = partition
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
            raise JanusParserException(
                original_text,
                f"The following segments are too long and must be "
                f"further subdivided:\n{problem_points}",
            )

        return "\n<JANUS_PARTITION>\n".join(chunks)
