import json
import re

from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers.json import parse_json_markdown
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel, Field

from janus.language.block import CodeBlock
from janus.parsers.parser import JanusParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class MultiDoc(BaseModel):
    docstring: str = Field(
        description="A Sphinx-style docstring for the code, including a summary "
        "of its functionality; the name, type, and description of "
        "any parameters or returns; and any potential exceptions "
        "that might arise in its execution"
    )
    example_usage: str = Field(
        description="A well-commented minimal example utilizing the given "
        "code's functionality"
    )
    pseudocode: str = Field(
        description="A Python-stype pseudocode implementation of the module or "
        "function's behavior"
    )


class MultiDocumentationParser(JanusParser, PydanticOutputParser):
    block_name: str = ""

    def __init__(self):
        PydanticOutputParser.__init__(self, pydantic_object=MultiDoc)

    def parse_input(self, block: CodeBlock) -> str:
        text = super().parse_input(block)
        self.block_name = str(block.name)
        return text

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)

        try:
            docs = json.loads(super().parse(text).json())
        except (OutputParserException, json.JSONDecodeError):
            log.debug(f"Invalid JSON object. Output:\n{text}")
            raise
        docs["name"] = self.block_name
        return json.dumps(docs)

    def parse_combined_output(self, text: str) -> str:
        """Parse the output text from the LLM when multiple inputs are combined.

        Arguments:
            text: The output text from the LLM.

        Returns:
            A parsed version of the text.
        """
        objs = [
            parse_json_markdown(line.strip()) for line in text.split("\n") if line.strip()
        ]
        output_obj = {d.pop("name"): d for d in objs}
        return json.dumps(output_obj)

    def get_format_instructions(self) -> str:
        """Get the format instructions for the parser.

        Returns:
            The format instructions for the LLM.
        """
        return (
            "Output must contain a sphinx-style docstring, example usage, and "
            "pseudocode, all in a json-formatted string with the following fields: "
            '"docstring", "example_usage", and "pseudocode".'
        )

    @property
    def _type(self) -> str:
        return str(self.__class__.name)


class MadlibsDocumentationParser(JanusParser):
    expected_keys: set[str]

    def __init__(self):
        super().__init__(expected_keys=[])

    def parse_input(self, block: CodeBlock) -> str:
        # TODO: Perform comment stripping/placeholding here rather than in script
        text = super().parse_input(block)
        comment_ids = re.findall(r"<(?:BLOCK|INLINE)_COMMENT (\w{8})>", text)
        self.expected_keys = set(comment_ids)
        return text

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)

        try:
            obj = parse_json_markdown(text)
        except json.JSONDecodeError as e:
            log.debug(f"Invalid JSON object. Output:\n{text}")
            raise OutputParserException(f"Got invalid JSON object. Error: {e}")

        if not isinstance(obj, dict):
            raise OutputParserException(
                f"Got invalid return object. Expected a dictionary, but got {type(obj)}"
            )

        seen_keys = set(obj.keys())
        missing_keys = self.expected_keys.difference(obj.keys())
        invalid_keys = seen_keys.difference(self.expected_keys)
        if missing_keys:
            log.debug(f"Missing keys: {missing_keys}")
            if invalid_keys:
                log.debug(f"Invalid keys: {invalid_keys}")
            log.debug(f"Missing keys: {missing_keys}")
            raise OutputParserException(
                f"Got invalid return object. Missing the following expected "
                f"keys: {missing_keys}"
            )

        for key in invalid_keys:
            del obj[key]

        for value in obj.values():
            if not isinstance(value, str):
                raise OutputParserException(
                    f"Got invalid return object. Expected all string values,"
                    f' but got type "{type(value)}"'
                )

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
        return str(self.__class__.name)
