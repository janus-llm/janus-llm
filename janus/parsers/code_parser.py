import re

from langchain.schema.output_parser import BaseOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser

from ..language.block import CodeBlock
from ..utils.logger import create_logger

log = create_logger(__name__)


class JanusParser:
    def parse_combined_output(self, text: str) -> str:
        """Parse the output text from the LLM when multiple inputs are combined

        Arguments:
            text: The output text from the LLM

        Returns:
            A parsed version of the text
        """
        if isinstance(text, BaseMessage):
            text = text.content
        return text

    def parse_into_block(self, text: str, block: CodeBlock):
        if isinstance(text, BaseMessage):
            text = text.content
        block.text = text

    def set_reference(self, block: CodeBlock):
        pass


class GenericParser(StrOutputParser, JanusParser):
    def parse(self, text: str) -> str:
        if isinstance(text, BaseMessage):
            return text.content
        return text


class CodeParser(BaseOutputParser[str], JanusParser):
    language: str

    def parse(self, text: str) -> str:
        if isinstance(text, BaseMessage):
            text = text.content
        pattern = rf"```[^\S\r\n]*(?:{self.language}[^\S\r\n]*)?\n?(.*?)\n*```"
        code = re.search(pattern, text, re.DOTALL)
        if code is None:
            raise OutputParserException(
                "Code not find code between triple square brackets"
            )
        return str(code.group(1))

    def get_format_instructions(self) -> str:
        return "Output must contain text contained within triple square brackets (```)"
