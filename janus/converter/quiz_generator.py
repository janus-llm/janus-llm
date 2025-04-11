from langchain_core.runnables import Runnable, RunnableParallel

from janus.converter.converter import Converter, run_if_changed
from janus.parsers.quiz_gen_parser import QuizGenParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class QuizGenerator(Converter):
    """A class that creates a multiple choice quiz about code."""

    def __init__(
        self,
        target_language: str = "json",
        target_version: str | None = "1.0",
        quiz_topic: str | None = "General",
        quiz_topic_description: str | None = "Questions about any aspect of the code.",
        **kwargs,
    ) -> None:
        """Initialize a Quiz Generator instance.

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set.
            model_arguments: Additional arguments to pass to the LLM constructor.
            source_language: The source programming language.
            target_language: The target programming language.
            target_version: The target version of the target programming language.
            max_prompts: The maximum number of prompts to try before giving up.
            max_tokens: The maximum number of tokens the model will take in.
                If unspecificed, model's default max will be used.
            prompt_templates: name of prompt template directories
                (see janus/prompts/templates) or paths to directories.
        """
        self._quiz_topic = quiz_topic
        self._quiz_topic_description = quiz_topic_description

        super().__init__(**kwargs)

        self.set_target_language(
            target_language=target_language,
            target_version=target_version,
        )

        self._load_parameters()

    def _load_parameters(self) -> None:
        self._load_parser()
        super()._load_parameters()

    @run_if_changed("_target_language")
    def _load_parser(self) -> None:
        """Load the parser according to this instance's attributes.

        If the relevant fields have not been changed since the last time this
        method was called, nothing happens.
        """
        self._parser = QuizGenParser(
            language=self._target_language, topic=self._quiz_topic
        )

    def _input_runnable(self) -> Runnable:
        return RunnableParallel(
            SOURCE_CODE=self._parser.parse_input,
            QUIZ_TOPIC=lambda x: self._quiz_topic,
            QUIZ_TOPIC_DESCRIPTION=lambda x: self._quiz_topic_description,
            context=self._retriever,
        )
