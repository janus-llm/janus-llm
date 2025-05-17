import json
import re

from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel, Field

from janus.language.block import CodeBlock
from janus.parsers.eval_parsers.inline_comment_parser import Criteria
from janus.parsers.parser import JanusParser
from janus.utils.logger import create_logger

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
        inputs["eval_object"] = re.findall(
            r"@startuml.*?@enduml",
            inputs["eval_object"],
            flags=re.DOTALL,
        )
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
