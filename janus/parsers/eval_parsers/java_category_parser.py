import json
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field, RootModel, ValidationError

from janus.language.block import CodeBlock
from janus.parsers.parser import JanusParserException, JsonParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class LabeledJava(BaseModel):
    start_line: int = Field(description="Start line of the code block")
    end_line: int = Field(description="End line of the code block")
    section_reasoning: str = Field(
        description="Brief reasoning for the evaluation of this block"
    )
    section_label: str = Field(
        description="Assigned label for the block",
        pattern=(
            r"^(non_code_text|lazy_implementation|placeholder_implementation|"
            r"commented_implementation|syntax_error|general_error|clean_implementation)$"
        ),
    )
    section_quality: int = Field(description="Integer score from 1 to 100")


class LabeledJavaList(RootModel):
    root: List[LabeledJava]


class LabeledJavaListParser(JsonParser, PydanticOutputParser):
    def __init__(self):
        PydanticOutputParser.__init__(self, pydantic_object=LabeledJavaList)

    @staticmethod
    def _add_line_numbers(code: str, start_line: int = 0) -> str:
        """Prefix each line of code with its line number."""
        return "\n".join(
            f"{i+start_line+1}    {line}" for i, line in enumerate(code.splitlines())
        )

    def parse_input(self, block: CodeBlock) -> str:
        text = super().parse_input(block)
        return self._add_line_numbers(text, block.start_point[0])

    def parse(self, text: str | BaseMessage) -> str:
        """Parse the text and return a JSON string representation."""
        if isinstance(text, BaseMessage):
            text = str(text.content)

        text = JsonParser.parse(self, text)
        objs = json.loads(text)
        log.info(f"Found {len(objs)} sections of labeled java code")

        if not isinstance(objs, list):
            raise OutputParserException(
                f"Expected a list of java labels, got {type(objs)}"
            )

        try:
            out: LabeledJavaList = PydanticOutputParser.parse(self, text)
        except json.JSONDecodeError as e:
            log.warning(f"Invalid JSON array. Output:\n{text}")
            raise OutputParserException(f"Got invalid JSON array. Error: {e}")
        except OutputParserException as e:
            log.warning(f"Pydantic parsing error. Output:\n{text}")
            raise JanusParserException(text, f"Pydantic parsing error: {e}")
        except ValidationError as e:
            log.warning(f"Validation error. Output:\n{text}")
            raise JanusParserException(text, f"Validation error: {e}")

        # JSON stringify
        serialized_output = json.dumps([obj.model_dump() for obj in out.root])
        log.debug(f"Serialized output:\n{serialized_output}")
        return serialized_output

    def parse_combined_output(self, text: str) -> str:
        json_parser = JsonParser()  # avoids method resolution conflict
        return json_parser.parse(text)
