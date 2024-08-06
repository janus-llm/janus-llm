import json

from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from typing import Literal

from ..language.block import CodeBlock
from ..utils.logger import create_logger
from .code_parser import JanusParser
import json
import re

from langchain.output_parsers.json import parse_json_markdown
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import AIMessage

log = create_logger(__name__)


class Eval(BaseModel):
    requirement: str = Field(description="The original requirment in the array")
    c1_necessary: Literal['pass', 'fail'] = Field(description="A score of either pass or fail for if the requirement is necessary")
    c2_appropriate: Literal['pass', 'fail'] = Field(description="A score of either pass or fail for if the requirement is appropriate")
    c3_unambiguous: Literal['pass', 'fail'] = Field(description="A score of either pass or fail for if the requirement is unambiguous")
    c4_complete: Literal['pass', 'fail'] = Field(description="A score of either pass or fail for if the requirement is complete")
    c5_singular: Literal['pass', 'fail'] = Field(description="A score of either pass or fail for if the requirement is singular")
    c6_feasible: Literal['pass', 'fail'] = Field(description="A score of either pass or fail for if the requirement is feasible")
    c7_verifiable: Literal['pass', 'fail'] = Field(description="A score of either pass or fail for if the requirement is verifiable")
    c8_correct: Literal['pass', 'fail'] = Field(description="A score of either pass or fail for if the requirement is correct")
    c9_conforming: Literal['pass', 'fail'] = Field(description="A score of either pass or fail for if the requirement is conforming")

    # You can add custom validation logic easily with Pydantic.
    # @validator("*")
    # def score_is_valid(cls, v: str):
    #     valid_scores = ["pass", "fail"]

    #     if v.lower() not in valid_scores:
    #         raise ValueError("Score must be either 'pass' or 'fail'")

    #     return v.lower()

    # TODO: include reasoning 

class EvaluationParser(PydanticOutputParser, JanusParser):
    block_name: str = ""

    def __init__(self):
        PydanticOutputParser.__init__(self, pydantic_object=Eval)

    def set_reference(self, block: CodeBlock):
        self.block_name = block.name

    def parse(self, text: str):
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