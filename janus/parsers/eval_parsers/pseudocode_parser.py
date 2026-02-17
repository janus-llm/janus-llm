import json

from langchain_core.exceptions import OutputParserException
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from janus.parsers.eval_parsers.inline_comment_parser import Criteria
from janus.parsers.parser import JanusParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class Pseudocode(BaseModel):
    completeness: Criteria = Field(description="The completeness of the pseudocode")
    hallucination: Criteria = Field(description="The factualness of the pseudocode")
    readability: Criteria = Field(description="The readability of the pseudocode")
    usefulness: Criteria = Field(description="The usefulness of the pseudocode")


class PseudocodeParser(JanusParser, PydanticOutputParser):
    def __init__(self):
        PydanticOutputParser.__init__(self, pydantic_object=Pseudocode)

    def parse(self, text: str | BaseMessage) -> str:
        # parsing the output evaluation object
        if isinstance(text, BaseMessage):
            text = str(text.content)

        # Strip everything outside the JSON object
        begin, end = text.find("{"), text.rfind("}")
        end += 1 if end != -1 else 0
        text = text[begin:end]

        try:
            out: Pseudocode = super(PseudocodeParser, self).parse(text)
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
