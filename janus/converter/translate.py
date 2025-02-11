from janus.converter.converter import Converter, run_if_changed
from janus.parsers.code_parser import CodeParser
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
        self._parser = CodeParser(language=self._target_language)
