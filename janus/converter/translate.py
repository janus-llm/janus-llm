from janus.converter.converter import Converter
from janus.converter.merge import MergedOutputConverterMixin
from janus.parsers.code_parser import IncompleteCodeParser
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
            prompt_template: name of prompt template directories
                (see janus/prompts/templates) or paths to directories.
        """
        super().__init__(
            target_language=target_language,
            target_version=target_version,
            **kwargs,
        )

        if target_language != "text":
            self._parser = IncompleteCodeParser(language=self._target_language)


class MergedOutputTranslator(MergedOutputConverterMixin, Translator):
    """A class that translates outputs from the OutputMerger to code."""

    def __init__(
        self,
        input_labels: set[str] | str | None = None,
        **kwargs,
    ) -> None:
        if input_labels is None:
            raise ValueError("MergedOutputTranslator requires input labels")
        super().__init__(
            input_labels=input_labels,
            **kwargs,
        )
