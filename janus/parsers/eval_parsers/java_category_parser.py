import json
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field, RootModel, ValidationError

from janus.language.block import CodeBlock
from janus.parsers.parser import JanusParser
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


class LabeledJavaListParser(JanusParser, PydanticOutputParser):
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

        begin, end = text.find("["), text.rfind("]")
        end += 1 if end != -1 else 0
        json_text = text[begin:end] # use text in debug later, dont overwrite

        try:
            parsed_data = json.loads(json_text)

            if not isinstance(parsed_data, list):
                raise OutputParserException(f"Expected a list, got {type(parsed_data)}")

            # let pydantic parse the list directly (will wrap it in '__root__')
            out: LabeledJavaList = LabeledJavaList(root=parsed_data)
        except json.JSONDecodeError as e:
            log.debug(f"Invalid JSON array. Output:\n{text}")
            raise OutputParserException(f"Got invalid JSON array. Error: {e}")
        except ValidationError as e:
            log.debug(f"Validation error. Output:\n{text}")
            raise OutputParserException(f"Validation error: {e}")

        # json stringify
        serialized_output = json.dumps([obj.model_dump() for obj in out.root])
        log.debug(f"Serialized output:\n{serialized_output}")
        return serialized_output

    def parse_combined_output(self, text: str) -> str:
        """Combine multiple JSON objects into a single JSON string."""
        if not text.strip():
            return "[]"
        
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        full_text = "[" + ",".join(lines) + "]"
        
        try:
            return self.parse(full_text)
        except OutputParserException as e:
            log.debug(f"Failed to parse combined output: {e}")
            return "[]"
