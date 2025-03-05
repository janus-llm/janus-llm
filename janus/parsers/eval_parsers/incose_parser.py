import json
import random
import uuid
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.messages import BaseMessage
from langchain_core.pydantic_v1 import BaseModel, Field, validator

from janus.language.block import CodeBlock
from janus.parsers.parser import JanusParser
from janus.utils.logger import create_logger

log = create_logger(__name__)
RNG = random.Random()


class Criteria(BaseModel):
    reasoning: str = Field(description="A short explanation for the given assessment")
    score: str = Field("A simple `pass` or `fail`")

    @validator("score")
    def score_is_valid(cls, v: str):
        v = v.lower().strip()
        if v not in {"pass", "fail"}:
            raise OutputParserException("Score must be either 'pass' or 'fail'")
        return v


class Requirement(BaseModel):
    requirement_id: str = Field(description="The 8-character comment ID")
    requirement: str = Field(description="The original requirement being evaluated")
    C1: Criteria
    C2: Criteria
    C3: Criteria
    C4: Criteria
    C5: Criteria
    C6: Criteria
    C7: Criteria
    C8: Criteria
    C9: Criteria


class RequirementList(BaseModel):
    __root__: List[Requirement] = Field(
        description=(
            "A list of requirement evaluations. Each element should include"
            " the requirement's 8-character ID in the `requirement_id` field,"
            " the original requirement in the 'requirement' field, "
            " and nine score objects corresponding to each criterion."
        )
    )


class IncoseParser(JanusParser, PydanticOutputParser):
    requirements: dict[str, str]

    def __init__(self):
        PydanticOutputParser.__init__(
            self,
            pydantic_object=RequirementList,
            requirements={},
        )

    def parse_input(self, block: CodeBlock) -> str:
        # TODO: Perform comment stripping/placeholding here rather than in script
        text = super().parse_input(block)
        RNG.seed(text)

        obj = json.loads(text)

        reqs = obj["requirements"]

        # Generate a unique ID for each requirement (ensure they are unique)
        req_ids = set()
        while len(req_ids) < len(reqs):
            req_ids.add(str(uuid.UUID(int=RNG.getrandbits(128), version=4))[:8])

        self.requirements = dict(zip(req_ids, reqs))
        reqs_str = "\n\n".join(
            f"Requirement {rid} : {req}" for rid, req in self.requirements.items()
        )
        obj["requirements"] = reqs_str
        return json.dumps(obj)

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)

        # Strip everything outside the JSON object
        begin, end = text.find("["), text.rfind("]")
        end += 1 if end != -1 else 0
        text = text[begin:end]

        try:
            out: RequirementList = super(IncoseParser, self).parse(text)
        except json.JSONDecodeError as e:
            log.debug(f"Invalid JSON object. Output:\n{text}")
            raise OutputParserException(f"Got invalid JSON object. Error: {e}")

        evals: dict[str, dict] = {c.requirement_id: c.dict() for c in out.__root__}

        seen_keys = set(evals.keys())
        expected_keys = set(self.requirements.keys())
        missing_keys = expected_keys.difference(seen_keys)
        invalid_keys = seen_keys.difference(expected_keys)
        if missing_keys:
            log.debug(f"Missing keys: {missing_keys}")
            if invalid_keys:
                log.debug(f"Invalid keys: {invalid_keys}")
            log.debug(f"Missing keys: {missing_keys}")
            raise OutputParserException(
                f"Got invalid return object. Missing the following expected "
                f"keys: {missing_keys}"
            )

        for key in invalid_keys:
            del evals[key]

        for rid in evals.keys():
            evals[rid]["requirement"] = self.requirements[rid]
            evals[rid].pop("requirement_id")

        return json.dumps(evals)

    def parse_combined_output(self, text: str) -> str:
        if not text.strip():
            return str({})
        objs = [json.loads(line.strip()) for line in text.split("\n") if line.strip()]
        output_obj = {}
        for obj in objs:
            output_obj.update(obj)
        return json.dumps(output_obj)
