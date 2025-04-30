import json
from typing import List, Any

from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from pydantic import ValidationError

from janus.language.block import CodeBlock
from janus.parsers.parser import JanusParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class LabeledJava(BaseModel):
    start_line: int = Field(description="Start line of the code block")
    end_line: int = Field(description="End line of the code block")
    section_reasoning: str = Field(description="Brief reasoning for the evaluation of this block")
    section_label: str = Field(
        description="Assigned label for the block",
        regex="^(non_code_text|lazy_implementation|placeholder_implementation|commented_implementation|syntax_error|general_error|clean_implementation)$"
    )
    section_quality: int = Field(description="Integer score from 1 to 100")

class LabeledJavaList(BaseModel):
    __root__: List[LabeledJava]

class LabeledJavaListParser(JanusParser, PydanticOutputParser):
    def __init__(self):
        PydanticOutputParser.__init__(self, pydantic_object=LabeledJavaList)

    def _add_line_numbers(self, code: str) -> str:
        """Prefix each line of code with its line number."""
        return "\n".join(f"{i+1}    {line}" for i, line in enumerate(code.splitlines()))

    def parse_input(self, block: CodeBlock) -> str:
        text = super().parse_input(block)
        return self._add_line_numbers(text)  # Add line numbers to help llm track evals

    def parse(self, text: str | BaseMessage) -> str:
        """Parse the text and return a JSON string representation."""
        if isinstance(text, BaseMessage):
            text = str(text.content)

        begin, end = text.find("["), text.rfind("]")
        end += 1 if end != -1 else 0
        text = text[begin:end]

        try:
            parsed_data = json.loads(text)
            if isinstance(parsed_data, list) and isinstance(parsed_data[0], list):
                parsed_data = [item for sublist in parsed_data for item in sublist]

            out: LabeledJavaList = super().parse(json.dumps({"__root__": parsed_data}))
        except json.JSONDecodeError as e:
            log.debug(f"Invalid JSON array. Output:\n{text}")
            raise OutputParserException(f"Got invalid JSON array. Error: {e}")
        except ValidationError as e:
            log.debug(f"Validation error. Output:\n{text}")
            raise OutputParserException(f"Validation error: {e}")

        # json stringify
        serialized_output = json.dumps([obj.dict() for obj in out.__root__])
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