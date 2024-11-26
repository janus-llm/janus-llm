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

log = create_logger(__name__)


class Criteria(BaseModel):
    reasoning: str = Field(description="A short explanation for the given score")
    # Constrained to an integer between 1 and 4
    score: conint(ge=1, le=4) = Field(  # type: ignore
        description="An integer score between 1 and 4 (inclusive), 4 being the best"
    )


class Comment(BaseModel):
    comment_id: str = Field(description="The 8-character comment ID")
    completeness: Criteria = Field(description="The completeness of the comment")
    hallucination: Criteria = Field(description="The factualness of the comment")
    readability: Criteria = Field(description="The readability of the comment")
    usefulness: Criteria = Field(description="The usefulness of the comment")


class CommentList(BaseModel):
    __root__: list[Comment] = Field(
        description=(
            "A list of inline comment evaluations. Each element should include"
            " the comment's 8-character ID in the `comment_id` field, and four"
            " score objects corresponding to each metric (`completeness`,"
            " `hallucination`, `readability`, and `usefulness`)."
        )
    )


class InlineCommentParser(JanusParser, PydanticOutputParser):
    comments: dict[str, str]

    def __init__(self):
        PydanticOutputParser.__init__(
            self,
            pydantic_object=CommentList,
            comments=[],
        )

    def parse_input(self, block: CodeBlock) -> str:
        # TODO: Perform comment stripping/placeholding here rather than in script
        text = super().parse_input(block)
        self.comments = dict(
            re.findall(
                r"<(?:BLOCK|INLINE)_COMMENT (\w{8})> (.*)$",
                text,
                flags=re.MULTILINE,
            )
        )
        return text

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)

        # Strip everything outside the JSON object
        begin, end = text.find("["), text.rfind("]")
        text = text[begin : end + 1]

        try:
            out: CommentList = super().parse(text)
        except json.JSONDecodeError as e:
            log.debug(f"Invalid JSON object. Output:\n{text}")
            raise OutputParserException(f"Got invalid JSON object. Error: {e}")

        evals: dict[str, Any] = {c.comment_id: c.dict() for c in out.__root__}

        seen_keys = set(evals.keys())
        expected_keys = set(self.comments.keys())
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

        for cid in evals.keys():
            evals[cid]["comment"] = self.comments[cid]
            evals[cid].pop("comment_id")

        return json.dumps(evals)

    def parse_combined_output(self, text: str) -> str:
        if not text.strip():
            return str({})
        objs = [json.loads(line.strip()) for line in text.split("\n") if line.strip()]
        output_obj = {}
        for obj in objs:
            output_obj.update(obj)
        return json.dumps(output_obj)
