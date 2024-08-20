import json
import re

from langchain.output_parsers.json import parse_json_markdown
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import BaseMessage

from janus.parsers.parser import JanusParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class RequirementsParser(JanusParser):
    expected_keys: set[str]

    def __init__(self):
        super().__init__(expected_keys=[])

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)

        # TODO: This is an incorrect implementation (lstrip and rstrip take character
        #       lists and strip any instances of those characters, not the full str)
        #       Should be replaced with a regex search, see CodeParser
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
            "Output must contain a requirements specification "
            "in a JSON-formatted string. The only key should be "
            "'requirements' and its value should be a JSON-formatted list "
            "containing the requirements."
        )

    @property
    def _type(self) -> str:
        return str(self.__class__.name)
