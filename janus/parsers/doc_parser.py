import json
import re

from langchain.output_parsers.json import parse_json_markdown
from langchain.schema.output_parser import BaseOutputParser
from langchain_core.exceptions import OutputParserException

from ..language.block import CodeBlock
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

    def get_format_instructions(self) -> str:
        """Get the format instructions for the parser.

        Returns:
            The format instructions for the LLM.
        """
        return (
            "Output must contain code description, input/output specification, and "
            'example code. The description should be enclosed in triple quotes ("""), '
            "the input/output specification in double brackets ([[]]), and the "
            "example code in triple backticks (```)."
        )

    @property
    def _type(self) -> str:
        return self.__class__.name


class MadlibsDocumentationParser(BaseOutputParser[str], JanusParser):
    expected_keys: set[str]

    def __init__(self):
        super().__init__(expected_keys=[])

    def set_reference(self, block: CodeBlock):
        comment_ids = re.findall(r"<(?:BLOCK|INLINE)_COMMENT (\w{8})>", block.text)
        self.expected_keys = set(comment_ids)

    def parse(self, text: str) -> str:
        try:
            obj = parse_json_markdown(text)
        except json.JSONDecodeError as e:
            raise OutputParserException(f"Got invalid JSON object. Error: {e}")

        seen_keys = set(obj.keys())
        missing_keys = self.expected_keys.difference(obj.keys())
        if missing_keys:
            raise OutputParserException(
                f"Got invalid return object. Missing the following expected "
                f"keys: {missing_keys}"
            )

        invalid_keys = seen_keys.difference(self.expected_keys)
        for key in invalid_keys:
            del obj[key]

        return json.dumps(obj)

    def parse_combined_output(self, text: str) -> str:
        """Parse the output text from the LLM when multiple inputs are combined.

        Arguments:
            text: The output text from the LLM.

        Returns:
            A parsed version of the text.
        """
        if not text.strip():
            return str({})
        objs = [
            parse_json_markdown(line.strip()) for line in text.split("\n") if line.strip()
        ]
        output_obj = {}
        for obj in objs:
            output_obj.update(obj)
        return json.dumps(output_obj)

    def get_format_instructions(self) -> str:
        """Get the format instructions for the parser.

        Returns:
            The format instructions for the LLM.
        """
        return (
            "Output must contain exactly one JSON-formatted block. The JSON "
            "object should contain only (and all of) the comment IDs present "
            "in the input code."
        )

    @property
    def _type(self) -> str:
        return self.__class__.name
