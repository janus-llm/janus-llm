from pathlib import Path
import json

from janus.converter.converter import Converter, run_if_changed
from janus.language.block import CodeBlock, TranslatedCodeBlock
from janus.parsers.quiz_taker_parser import QuizTakerParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class QuizTaker(Converter):
    """A class that translates code from one programming language into a multiple choice quiz."""

    def __init__(
        self,
        target_language: str = "json",
        target_version: str | None = "1.0",
        **kwargs,
    ) -> None:
        """Initialize a Quiz Taker instance.

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
        self._parser = QuizTakerParser(language=self._target_language)


    def translate_block(self, input_block: CodeBlock, failure_path: Path | None = None):
        self._load_parameters()
        # Strip answers from quiz "correct-answer-number" before input
        stripped_input_block = input_block
        data = json.loads(input_block.text)
        for question in data:
            if "correct-answer-number" in question:
                del question["correct-answer-number"]
        stripped_data = json.dumps(data)
        stripped_input_block.text = stripped_data
        # Input stripped input into normal translate process
        output_block = self._iterative_translate(stripped_input_block, failure_path)
        if output_block.translated:
            completeness = output_block.translation_completeness
            log.info(
                f"[{output_block.name}] Translation complete\n"
                f"  {completeness:.2%} of input successfully translated\n"
                f"  Total cost: ${output_block.total_cost:,.2f}\n"
                f"  Output CodeBlock Structure:\n{stripped_input_block.tree_str()}\n"
            )

        else:
            log.error(
                f"[{output_block.name}] Translation failed\n"
                f"  Total cost: ${output_block.total_cost:,.2f}\n"
            )
        return output_block
