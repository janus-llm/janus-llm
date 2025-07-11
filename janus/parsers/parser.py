import json

from langchain.schema.output_parser import BaseOutputParser
from langchain_core.exceptions import OutputParserException
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


class JsonParser(JanusParser):
    @staticmethod
    def extract_json_objects(text, decoder=json.JSONDecoder()):
        """Find JSON objects and arrays in text, and yield the decoded JSON data"""
        pos = 0
        while True:
            obj_match = text.find("{", pos)
            arr_match = text.find("[", pos)

            # If both searches failed, there are no more objects or arrays
            if obj_match < 0 and arr_match < 0:
                break

            # If one search failed, take the one that didn't
            if obj_match < 0 or arr_match < 0:
                match = max(obj_match, arr_match)

            # Otherwise, take the match closer to the start of the string
            else:
                match = min(obj_match, arr_match)

            try:
                result, index = decoder.raw_decode(text[match:])
                yield result
                pos = match + index
            except ValueError:
                pos = match + 1

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)
        objs = list(self.extract_json_objects(text))
        if not objs:
            raise JanusParserException(text, "Found no valid JSON object(s)")
        # If a top-level object is a list, flatten
        objs = [x for obj in objs for x in (obj if isinstance(obj, list) else [obj])]
        return json.dumps(objs)

    def parse_combined_output(self, text: str) -> str:
        # Parse should handle JSONL text just fine
        return self.parse(text)

    def get_format_instructions(self) -> str:
        return "Output should contain one or more JSON objects"


class JanusParserException(OutputParserException):
    def __init__(self, unparsed_output, *args, **kwargs):
        self.unparsed_output = unparsed_output
        super().__init__(*args, **kwargs)
