import json

from langchain_core.exceptions import OutputParserException
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, conint

from janus.parsers.parser import JanusParserException, JsonParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class Criteria(BaseModel):
    reasoning: str = Field(description="A short explanation for the given score")
    # Constrained to an integer between 1 and 100
    score: conint(ge=1, le=100) = Field(  # type: ignore
        description="An integer score between 1 and 100 (inclusive), 100 being the best"
    )


class Evaluation(BaseModel):
    completeness: Criteria = Field(description="The completeness of the artifact")
    hallucination: Criteria = Field(description="The factualness of the artifact")
    readability: Criteria = Field(description="The readability of the artifact")
    usefulness: Criteria = Field(description="The usefulness of the artifact")


class GenericEvaluationParser(JsonParser, PydanticOutputParser):
    def __init__(self):
        PydanticOutputParser.__init__(self, pydantic_object=Evaluation)

    def parse(self, text: str | BaseMessage) -> str:
        # parsing the output evaluation object
        if isinstance(text, BaseMessage):
            text = str(text.content)

        # Strip everything outside the JSON object
        text = JsonParser.parse(self, text)
        objs = json.loads(text)
        if len(objs) > 1:
            log.warning(f"Expected single evaluation object, recieved {len(objs)}")
            raise JanusParserException(
                text, f"Expected single evaluation object, recieved {len(objs)}"
            )
        text = json.dumps(objs[0])

        try:
            out: Evaluation = PydanticOutputParser.parse(self, text)
        except json.JSONDecodeError as e:
            log.warning(f"Invalid JSON object. Output:\n{text}")
            raise OutputParserException(f"Got invalid JSON object. Error: {e}")
        except OutputParserException as e:
            log.warning(f"Pydantic parsing error. Output:\n{text}")
            raise JanusParserException(text, f"Pydantic parsing error: {e}")

        return out.model_dump_json()

    def parse_combined_output(self, text: str) -> str:
        return JsonParser.parse(self, text)
