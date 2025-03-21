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
        text = super().parse_input(block)
        inputs = json.loads(text)
        # strong assumption every @startuml has an @enduml, aka valid uml
        diagram_str = inputs["diagrams"]
        start_indicies = []
        end_indicies = []
        start = 0
        index = 0
        end = len(diagram_str)
        while index != -1:
            index = diagram_str.find("@st", start)
            if index != -1:
                start_indicies.append(index)
                start = index + 3
                end_indicies.append(diagram_str.rfind("@enduml", end))
                end = end_indicies[-1] - 3
        
        if len(start_indicies) == 1:
            inputs["diagrams"] = [diagram_str]
            return json.dumps(inputs)
        
        diagram_list = []
        for i, idx in enumerate(start_indicies):
            end_idx = end_indicies[-1-i]
            end_idx += 1
            diagram_list.append(diagram_str[idx:end_idx])
        print(diagram_list)
        inputs["diagrams"] = diagram_list
        return json.dumps(inputs)
    
    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)

        # Strip everything outside the JSON object, do I need this?
        begin, end = text.find("{"), text.rfind("}")
        end += 1 if end != -1 else 0
        text = text[begin:end]

        try:
            out: Diagram = super(UMLParser, self).parse(text)
        except json.JSONDecodeError as e:
            log.debug(f"Invalid JSON object. Output:\n{text}")
            raise OutputParserException(f"Got invalid JSON object. Error: {e}")

        return out.json()
    
    def parse_combined_output(self, text: str) -> str:
        if not text.strip():
            return str({})
        objs = [json.loads(line.strip()) for line in text.split("\n") if line.strip()]
        output_obj = {}
        for obj in objs:
            output_obj.update(obj)
        return json.dumps(output_obj)