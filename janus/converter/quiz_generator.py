from langchain_core.runnables import Runnable, RunnableParallel

from janus.converter.converter import Converter
from janus.parsers.quiz_gen_parser import QuizGenParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class QuizGenerator(Converter):
    """A class that creates a multiple choice quiz about code."""

    def __init__(
        self,
        prompt_template: str = "quiz/quiz_generator",
        target_language: str = "json",
        quiz_topic: str = "General",
        quiz_topic_description: str = "Questions about any aspect of the code.",
        combine_output: bool = False,
        **kwargs,
    ) -> None:
        if combine_output:
            raise ValueError("`combine_output` not supported")
        super().__init__(
            target_language=target_language,
            prompt_template=prompt_template,
            combine_output=combine_output,
            **kwargs,
        )

        self._quiz_topic = quiz_topic
        self._quiz_topic_description = quiz_topic_description
        self._parser = QuizGenParser(
            language=target_language,
            topic=quiz_topic,
        )

    def _input_runnable(self) -> Runnable:
        return RunnableParallel(
            SOURCE_CODE=self._parser.parse_input,
            QUIZ_TOPIC=lambda x: self._quiz_topic,
            QUIZ_TOPIC_DESCRIPTION=lambda x: self._quiz_topic_description,
            context=self._retriever,
        )
