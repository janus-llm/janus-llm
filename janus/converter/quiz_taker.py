import json

from langchain_core.runnables import Runnable, RunnableParallel
from langchain_core.runnables.passthrough import RunnablePick

from janus.converter.converter import Converter
from janus.parsers.quiz_taker_parser import QuizTakerParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


def extract_from_json(key: str):
    def _extract(json_text: str) -> str:
        return json.loads(json_text)[key]

    return _extract


class QuizTaker(Converter):
    """A class that takes a multiple choice quiz about code."""

    def __init__(
        self,
        prompt_template: str = "quiz/quiz_taker",
        target_language: str = "json",
        **kwargs,
    ) -> None:
        super().__init__(
            target_language=target_language, prompt_template=prompt_template, **kwargs
        )

        self._parser = QuizTakerParser(language=target_language)

    def _input_runnable(self) -> Runnable:
        return RunnableParallel(
            json=self._parser.parse_input, context=self._retriever
        ) | RunnableParallel(
            QUIZ=RunnablePick("json") | extract_from_json("quiz"),
            SOURCE_CODE=RunnablePick("json") | extract_from_json("code"),
            context=RunnablePick("context"),
        )
