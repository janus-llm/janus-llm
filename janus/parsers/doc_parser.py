import json
import re

from langchain.schema.output_parser import BaseOutputParser
from langchain_core.exceptions import OutputParserException

from ..utils.logger import create_logger
from .code_parser import JanusParser

log = create_logger(__name__)


class DocumentationParser(BaseOutputParser[str], JanusParser):
    def parse(self, text: str) -> str:
        """Parse the JSON object, convert keys to lowercase, filter out
        unexpected keys

        Arguments:
            text: The output text from the LLM.

        Returns:
            A parsed version of the text.
        """
        description = r'"""(.*?)"""'
        input_output = r"\[\[(.*?)\]\]"
        example_code = r"```(.*?)```"
        documentation = rf"{description}\s*{input_output}\s*{example_code}"
        match = re.search(documentation, text, re.DOTALL)
        if match is None:
            raise OutputParserException("Missing some piece of documentation")

        obj = dict(
            description=match.group(1).strip(),
            input_output=match.group(2).strip(),
            example_code=match.group(3).strip(),
        )
        return json.dumps(obj)

    def parse_combined_output(self, text: str) -> str:
        """Parse the JSON object, convert keys to lowercase, filter out
        unexpected keys, and average the values

        Arguments:
            text: The output text from the LLM.

        Returns:
            A parsed version of the text.
        """
        description = r'"""(.*?)"""'
        input_output = r"\[\[(.*?)\]\]"
        example_code = r"```(.*?)```"
        documentation = rf"{description}\s*{input_output}\s*{example_code}"
        matches = re.findall(documentation, text, re.DOTALL)

        objs = [
            dict(
                description=a.strip(),
                input_output=b.strip(),
                example_code=c.strip(),
            )
            for a, b, c in matches
        ]
        return json.dumps(objs)
