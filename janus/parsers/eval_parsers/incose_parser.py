import json

from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import Literal, List

from ...utils.logger import create_logger
from ..code_parser import JanusParser
import json
import re

from langchain.output_parsers.json import parse_json_markdown
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import AIMessage

log = create_logger(__name__)
class Criteria(BaseModel):
    reasoning: str
    score: Literal["pass", "fail"]

class Requirement(BaseModel):
    requirement: str
    C1: Criteria
    C2: Criteria
    C3: Criteria
    C4: Criteria
    C5: Criteria
    C6: Criteria
    C7: Criteria
    C8: Criteria
    C9: Criteria

class Requirement(BaseModel):
    requirements: List[Requirement]

class IncoseParser(PydanticOutputParser, JanusParser):
    block_name: str = ""

    def __init__(self):
        PydanticOutputParser.__init__(self, pydantic_object=Requirement)

    # need to parse off input and get the number of inputs and then then check to see if List[requirements].size matches
    # def set_reference(self, block: CodeBlock):
        # self.block_name = block.name

    def parse(self, text: str):
        if isinstance(text, AIMessage):
            text = text.content
        text = text.lstrip("```json") # change this to a regex or check for json in the front 
        text = text.rstrip("`")
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
    
    def get_format_instructions(self) -> str:
        """Get the format instructions for the parser.

        Returns:
            The format instructions for the LLM.
        """
        return (
            "Output must contain a all original requirements specification"
            "in a JSON-formatted string. For each and every requirment there should be evaluated crieteria C1-C9 each including:"
            "1) The LLM reasoning behind the score."
            "2) The 'Score' of either a 'pass' or 'fail'"
        )