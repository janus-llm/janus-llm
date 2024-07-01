import json
import re

from langchain.output_parsers.json import parse_json_markdown
from langchain.schema.output_parser import BaseOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import AIMessage

from ..language.block import CodeBlock
from ..utils.logger import create_logger
from .code_parser import JanusParser

log = create_logger(__name__)


class RequirementsParser(BaseOutputParser[str], JanusParser):
    block_name: str = ""

    def __init__(self):
        super().__init__(expected_keys=[])

    def set_reference(self, block: CodeBlock):
        self.block_name = block.name

    def parse(self, text: str) -> str:
        if isinstance(text, AIMessage):
            text = text.content
        text = text.lstrip("```json")
        text = text.rstrip("```")
        try:
            obj = parse_json_markdown(text)
        except json.JSONDecodeError as e:
            log.debug(f"Invalid JSON object. Output:\n{text}")
            raise OutputParserException(f"Got invalid JSON object. Error: {e}")

        if not isinstance(obj, dict):
            raise OutputParserException(
                f"Got invalid return object. Expected a dictionary, but got {type(obj)}"
            )
        return json.dumps(obj)

    def parse_combined_output(self, text: str):
        """Parse the output text from the LLM when multiple inputs are combined.

        Arguments:
            text: The output text from the LLM.

        Returns:
            A parsed version of the text.
        """
        json_strings = re.findall(r"\{.*?\}", text)
        output_list = list()
        for i, json_string in enumerate(json_strings, 1):
            json_dict = json.loads(json_string)
            output_list.append(json_dict["requirements"])
        return output_list

    def get_format_instructions(self) -> str:
        """Get the format instructions for the parser.

        Returns:
            The format instructions for the LLM.
        """
        return (
            "Output must contain an ieee style requirements specification "
            "all in a json-formatted string, including the following field: "
            '"requirements".'
        )

    @property
    def _type(self) -> str:
        return self.__class__.name
