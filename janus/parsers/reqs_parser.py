import json
import re

from langchain.output_parsers.json import parse_json_markdown
from langchain_core.messages import BaseMessage

from janus.parsers.parser import JanusParser, JanusParserException
from janus.utils.logger import create_logger

log = create_logger(__name__)


class RequirementsParser(JanusParser):
    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)
        original_text = text

        pattern = r"```[^\S\r\n]*(?:json[^\S\r\n]*)?\n?(.*?)\n*```"
        match = re.search(pattern, text, re.DOTALL)
        if match is None:
            raise JanusParserException(
                original_text,
                "Output object not contained between triple backtick delimiters (```)",
            )

        text = str(match.group(1))
        try:
            obj = parse_json_markdown(text)
        except json.JSONDecodeError as e:
            log.debug(f"Invalid JSON object. Output:\n{text}")
            raise JanusParserException(
                original_text,
                f"Got invalid JSON object. Error: {e}",
            )

        if not isinstance(obj, dict):
            raise JanusParserException(
                original_text,
                f"Got invalid return object. Expected a dictionary, but got {type(obj)}",
            )

        if "requirements" not in obj or len(obj.keys()) != 1:
            raise JanusParserException(
                original_text,
                "Return object expected to contain a single key, 'requirements'",
            )

        return json.dumps(obj)

    def parse_combined_output(self, text: str) -> str:
        """Parse the output text from the LLM when multiple inputs are combined.

        Arguments:
            text: The output text from the LLM.

        Returns:
            A parsed version of the text.
        """
        json_strings = re.findall(r"\{.*?\}", text)
        output_list = list()
        for _, json_string in enumerate(json_strings, 1):
            json_dict = json.loads(json_string)
            output_list.extend(json_dict["requirements"])
        obj = {"requirements": output_list}
        return json.dumps(obj)

    def get_format_instructions(self) -> str:
        """Get the format instructions for the parser.

        Returns:
            The format instructions for the LLM.
        """
        return (
            "Output must by formatted as a JSON object. The only key should be"
            " 'requirements' and its value should be a JSON-formatted list of"
            " strings, each string specifying a single requirement. Wrap the JSON"
            " object in annotated triple backticks (```)."
        )

    @property
    def _type(self) -> str:
        return str(self.__class__.name)
