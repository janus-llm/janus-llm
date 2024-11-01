from langchain.schema.output_parser import BaseOutputParser
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser

from janus.language.block import CodeBlock
from janus.language.splitter import EmptyTreeError
from janus.utils.logger import create_logger

log = create_logger(__name__)


class JanusParser(BaseOutputParser[str]):
    def parse_input(self, block: CodeBlock) -> str:
        """Parse the input block into raw string input ready to be passed to
        an LLM. Also perform any processing or saving of metadata.

        Arguments:
            block: The CodeBlock to be processed

        Returns:
            A parsed version of the input text
        """
        if block.text is None:
            raise EmptyTreeError("No text in input CodeBlock!")
        return block.text

    def parse_combined_output(self, text: str) -> str:
        """Parse the output text from the LLM when multiple inputs are combined

        Arguments:
            text: The output text from the LLM

        Returns:
            A parsed version of the text
        """
        return text

    def parse_into_block(self, text: str | BaseMessage, block: CodeBlock):
        if isinstance(text, BaseMessage):
            text = str(text.content)
        block.text = text


class GenericParser(JanusParser, StrOutputParser):
    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)
        return text

    def get_format_instructions(self) -> str:
        return "Output should be a string"
