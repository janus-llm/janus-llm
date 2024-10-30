from janus.converter.converter import Converter, run_if_changed
from janus.llm.models_info import MODEL_PROMPT_ENGINES
from janus.parsers.code_parser import CodeParser
from janus.prompts.prompt import SAME_OUTPUT
from janus.utils.enums import LANGUAGES
from janus.utils.logger import create_logger

log = create_logger(__name__)


class Translator(Converter):
    """A class that translates code from one programming language to another."""

    def __init__(
        self,
        target_language: str = "python",
        target_version: str | None = "3.10",
        **kwargs,
    ) -> None:
        """Initialize a Translator instance.

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set and the
                `OPENAI_ORG_ID` environment variable should be set if needed.
            model_arguments: Additional arguments to pass to the LLM constructor.
            source_language: The source programming language.
            target_language: The target programming language.
            target_version: The target version of the target programming language.
            max_prompts: The maximum number of prompts to try before giving up.
            max_tokens: The maximum number of tokens the model will take in.
                If unspecificed, model's default max will be used.
            prompt_template: name of prompt template directory
                (see janus/prompts/templates) or path to a directory.
        """
        super().__init__(**kwargs)

        self._target_version: str | None

        self.set_target_language(
            target_language=target_language,
            target_version=target_version,
        )

        self._load_parameters()

    def _load_parameters(self) -> None:
        self._load_parser()
        super()._load_parameters()

    def set_target_language(
        self, target_language: str, target_version: str | None
    ) -> None:
        """Validate and set the target language.

        The affected objects will not be updated until translate() is called.

        Arguments:
            target_language: The target programming language.
            target_version: The target version of the target programming language.
        """
        target_language = target_language.lower()
        if target_language not in LANGUAGES:
            raise ValueError(
                f"Invalid target language: {target_language}. "
                "Valid target languages are found in `janus.utils.enums.LANGUAGES`."
            )
        self._target_language = target_language
        self._target_version = target_version
        self._target_suffix = f".{LANGUAGES[target_language]['suffix']}"

    @run_if_changed(
        "_prompt_template_name",
        "_source_language",
        "_target_language",
        "_target_version",
        "_model_name",
    )
    def _load_prompt(self) -> None:
        """Load the prompt according to this instance's attributes.

        If the relevant fields have not been changed since the last time this
        method was called, nothing happens.
        """
        if self._prompt_template_name in SAME_OUTPUT:
            if self._target_language != self._source_language:
                raise ValueError(
                    f"Prompt template ({self._prompt_template_name}) suggests "
                    f"source and target languages should match, but do not "
                    f"({self._source_language} != {self._target_language})"
                )

        prompt_engine = MODEL_PROMPT_ENGINES[self._llm.short_model_id](
            source_language=self._source_language,
            target_language=self._target_language,
            target_version=self._target_version,
            prompt_template=self._prompt_template_name,
        )
        self._prompt = prompt_engine.prompt

    @run_if_changed("_target_language")
    def _load_parser(self) -> None:
        """Load the parser according to this instance's attributes.

        If the relevant fields have not been changed since the last time this
        method was called, nothing happens.
        """
        self._parser = CodeParser(language=self._target_language)
