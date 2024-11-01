import json
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers.json import parse_json_markdown
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import AIMessage
from langchain_core.pydantic_v1 import BaseModel, conint

from janus.parsers.parser import JanusParser

from ...utils.logger import create_logger

log = create_logger(__name__)


class Criteria(BaseModel):
    reasoning: str
    # Constrained to an integer between 1 and 4
    score: conint(ge=1, le=4)  # type: ignore


class Comment(BaseModel):
    comment: str
    Completeness: Criteria
    Hallucination: Criteria
    Readability: Criteria
    Usefulness: Criteria


class CommentList(BaseModel):
    comments: List[Comment]


class InlineCommentParser(PydanticOutputParser, JanusParser):
    block_name: str = ""
    input_length: int = 0  # Define input_length as a Pydantic field with a default value

    def __init__(self):
        super().__init__(pydantic_object=CommentList)
        self.input_length = 0  # Initialize input_length in the constructor

    def parse(self, text: str):
        log.info("Parsing text...")
        if isinstance(text, AIMessage):
            text = text.content
        text = text.lstrip(
            "```json"
        )  # change this to a regex or check for json in the front
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
        # move the check into this method
        return json.dumps(obj)

    def get_format_instructions(self) -> str:
        """Get the format instructions for the parser."""
        return (
            "Output must contain all original comments specifications "
            "in a JSON-formatted string. For each and every comment "
            "there should be evaluated criteria  Completeness, "
            "Hallucination, Readability, and Usefulness each including: "
            "1) The LLM reasoning behind the score. "
            "2) The 'Score' of either a 1,2,3, or 4'."
            "Continue generating your response until all comments have been returned. "
        )
