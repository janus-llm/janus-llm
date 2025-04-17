import json

from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel

from janus.converter.converter import Converter
from janus.parsers.quiz_taker_parser import QuizTakerParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class QuizTaker(Converter):
    """A class that takes a multiple choice quiz about code."""

    def __init__(
        self,
        target_language: str = "json",
        **kwargs,
    ) -> None:
        super().__init__(target_language=target_language, **kwargs)

        self._parser = QuizTakerParser(language=target_language)

    def _input_runnable(self) -> Runnable:
        def _get_quiz(json_text: str) -> str:
            return json.loads(json_text)["quiz"]

        def _get_code(json_text: str) -> str:
            return json.loads(json_text)["code"]

        return RunnableLambda(self._parser.parse_input) | RunnableParallel(
            QUIZ=_get_quiz,
            SOURCE_CODE=_get_code,
            # TODO ADD TOPIC?
            context=self._retriever,
        )
