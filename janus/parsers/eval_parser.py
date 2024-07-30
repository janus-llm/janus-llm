import json

from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field, validator

from ..utils.logger import create_logger
from .code_parser import JanusParser

log = create_logger(__name__)


class Eval(BaseModel):
    syntax: float = Field(description="A numeric score (0-4) for code syntax")
    style: float = Field(description="A numeric score (0-4) for code style")
    completeness: float = Field(description="A numeric score (0-4) for code completeness")
    correctness: float = Field(description="A numeric score (0-4) for code correctness")

    # You can add custom validation logic easily with Pydantic.
    @validator("*")
    def score_is_valid(cls, v: float | int):
        try:
            v = float(v)
        except ValueError:
            raise ValueError("must be a number")

        if not 0 <= v <= 4:
            raise ValueError("must be a value between 0 and 4 inclusive")

        return v

    def __add__(self, other):
        if isinstance(other, int) and other == 0:
            return self.copy()
        return Eval.construct(
            syntax=self.syntax + other.syntax,
            style=self.style + other.style,
            correctness=self.correctness + other.correctness,
            completeness=self.completeness + other.completeness,
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __truediv__(self, other):
        if isinstance(other, int):
            return Eval.construct(
                syntax=self.syntax / other,
                style=self.style / other,
                correctness=self.correctness / other,
                completeness=self.completeness / other,
            )
        return Eval.construct(
            syntax=self.syntax / other.syntax,
            style=self.style / other.style,
            correctness=self.correctness / other.correctness,
            completeness=self.completeness / other.completeness,
        )


class EvaluationParser(PydanticOutputParser, JanusParser):
    def __init__(self):
        PydanticOutputParser.__init__(self, pydantic_object=Eval)

    def parse(self, text: str) -> str:
        eval = super().parse(text)
        return json.dumps(eval.json())

    def parse_combined_output(self, text: str) -> str:
        """Parse the JSON object, convert keys to lowercase, filter out
        unexpected keys, and average the values

        Arguments:
            text: The output text from the LLM.

        Returns:
            A parsed version of the text.
        """
        objs = [super().parse(line.strip()) for line in text.split("\n")]
        avg_obj = sum(objs) / len(objs)
        return json.dumps(avg_obj.json())
