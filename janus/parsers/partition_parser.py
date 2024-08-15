import json
import random
import uuid

from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
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
    lines: list[str] = []
    line_id_to_index: dict[str, int] = {}

    def __init__(self, token_limit: int):
        PydanticOutputParser.__init__(
            self, token_limit=token_limit, pydantic_object=PartitionList
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

        split_points = {0}
        for partition in out.__root__:
            if partition.location not in self.line_id_to_index:
                raise OutputParserException(
                    f"Line ID not found in input: {partition.location}"
                )
            split_points.add(self.line_id_to_index[partition.location])

        split_points = sorted(split_points) + [-1]
        chunks = [
            "\n".join(self.lines[i0:i1]) for i0, i1 in zip(split_points, split_points[1:])
        ]
        return "\n<JANUS_PARTITION>\n".join(chunks)
