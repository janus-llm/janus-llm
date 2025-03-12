import json
import re
from typing import Any

from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel, Field, conint

from janus.language.block import CodeBlock
from janus.parsers.parser import JanusParser
from janus.utils.logger import create_logger
from janus.parsers.eval_parsers.inline_comment_parser import Criteria

log = create_logger(__name__)

class Diagram(BaseModel):
    #diagram_id: str = Field(description="The 8-character diagram ID")
    completeness: Criteria = Field(description="The completeness of the diagram")
    hallucination: Criteria = Field(description="The factualness of the diagram")
    readability: Criteria = Field(description="The readability of the diagram")
    usefulness: Criteria = Field(description="The usefulness of the diagram")

class UMLParser(JanusParser, PydanticOutputParser):
    diagrams: dict[str, str]

    def __init__(self):
        PydanticOutputParser.__init__(
            self,
            pydantic_object=Diagram,
            diagrams={},
        )

    def parse_input(self, block: CodeBlock) -> str:
        text = ""

        return text
    
    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)

        return text
    
    def parse_combined_output(self, text: str) -> str:
        if not text.strip():
            return str({})
        objs = [json.loads(line.strip()) for line in text.split("\n") if line.strip()]
        output_obj = {}
        for obj in objs:
            output_obj.update(obj)
        return json.dumps(output_obj)