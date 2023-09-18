from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Tuple

from .language.block import CodeBlock, TranslatedCodeBlock
from .language.combine import Combiner
from .language.mumps import MumpsSplitter
from .language.treesitter import TreeSitterSplitter
from .llm import (
    COST_PER_MODEL,
    MODEL_CONSTRUCTORS,
    MODEL_DEFAULT_ARGUMENTS,
    TOKEN_LIMITS,
)
from .parsers.code_parser import CodeParser
from .prompts.prompt import SAME_OUTPUT, TEXT_OUTPUT, PromptEngine
from .utils.enums import CUSTOM_SPLITTERS, LANGUAGES
from .utils.logger import create_logger

log = create_logger(__name__)

VALID_MODELS: Tuple[str, ...] = tuple(MODEL_CONSTRUCTORS.keys())


class Translator:
    """A class that translates code from one programming language to another."""

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        model_arguments: Dict[str, Any] = {},
        source_language: str = "fortran",
        target_language: str = "python",
        target_version: str = "3.10",
        max_prompts: int = 10,
        prompt_template: str = "simple",
    ) -> None:
        """Initialize a Translator instance.

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set and the
                `OPENAI_ORG_ID` environment variable should be set if needed.
            source_language: The source programming language.
            target_language: The target programming language.
            target_version: The target version of the target programming language.
            max_prompts: The maximum number of times to prompt a model on one functional
                block.
            prompt_template: name of prompt template directory
                (see janus/prompts/templates) or path to a directory.
        """
        self.model = model.lower()
        self.model_arguments = model_arguments
        self.source_language = source_language.lower()
        self.target_language = target_language.lower()
        self.target_version = target_version
        self.max_prompts = max_prompts
        self.prompt_template = prompt_template
        self._check_languages()
        self._load_model()
        self._load_splitter()
        self._load_combiner()
        self._load_prompt_engine()
        self._load_parser()

    def translate(
        self, input_directory: str | Path, output_directory: str | Path
    ) -> None:
        """Translate code from the source language to the target language.

        Arguments:
            input_directory: The directory containing the code to translate.
            output_directory: The directory to write the translated code to.
        """
        # Convert paths to pathlib Paths if needed
        if isinstance(input_directory, str):
            input_directory = Path(input_directory)
        if isinstance(output_directory, str):
            output_directory = Path(output_directory)

        # Make sure the output directory exists
        if not output_directory.exists():
            output_directory.mkdir(parents=True)

        # Ensure that output languages are set to expected values for prompts
        if self.prompt_template in TEXT_OUTPUT and "text" != self.target_language:
            # Text outputs for documentation, requirements, etc.
            self.target_language = "text"
        if (
            self.prompt_template in SAME_OUTPUT
            and self.target_language != self.source_language
        ):
            # Document inline should output the same as the input
            self.target_language = self.source_language

        source_suffix = LANGUAGES[self.source_language]["suffix"]
        target_suffix = LANGUAGES[self.target_language]["suffix"]

        files = list(input_directory.glob(self._glob))
        files = [
            f
            for f in files
            if not (output_directory / f.with_suffix(f".{target_suffix}").name).exists()
        ]
        translated_files = map(self.translate_file, files)

        # Now, loop through every code block in every file and translate it with an LLM
        total_cost = 0.0
        for out_block in translated_files:
            total_cost += out_block.total_cost
            if not out_block.translated:
                continue

            # Write the code blocks to the output file
            out_block.path = output_directory / out_block.original.path.name.replace(
                f".{source_suffix}", f".{target_suffix}"
            )
            self.combiner.combine_children(out_block)
            self._save_to_file(out_block)

        log.info(f"Total cost: ${total_cost:,.2f}")

    def translate_file(self, file: Path) -> TranslatedCodeBlock:
        filename = file.name
        log.info(f"[{filename}] Splitting file")
        input_block = self.splitter.split(file)
        log.info(
            f"[{filename}] File split into {input_block.n_descendents:,} blocks, "
            f"tree of height {input_block.height}"
        )
        output_block = self._iterative_translate(input_block)
        if output_block.translated:
            completeness = output_block.total_input_tokens / input_block.total_tokens
            log.info(
                f"[{filename}] Translation complete\n"
                f"  {completeness:.2%} of input successfully translated\n"
                f"  Total cost: ${output_block.total_cost:,.2f}\n"
                f"  Total retries: {output_block.total_retries:,d}\n"
            )
        else:
            log.error(
                f"[{filename}] Translation failed\n"
                f"  Total cost: ${output_block.total_cost:,.2f}\n"
                f"  Total retries: {output_block.total_retries:,d}\n"
            )
        return output_block

    def _iterative_translate(self, root: CodeBlock) -> TranslatedCodeBlock:
        translated_root = TranslatedCodeBlock.from_original(root, self.target_language)
        last_prog, prog_delta = 0, 0.1
        stack = [translated_root]
        while stack:
            translated_block = stack.pop()
            self._add_translation(translated_block)
            if not translated_block.translated:
                continue

            for child in translated_block.original.children:
                # Don't bother translating children if they aren't used
                if self.combiner.contains_child(translated_block.code, child):
                    translated_child = TranslatedCodeBlock.from_original(
                        child, self.target_language
                    )
                    translated_block.children.append(translated_child)
                    stack.append(translated_child)
                else:
                    log.warning(f"Skipping {child.id} (not referenced in parent code)")

            progress = translated_root.total_input_tokens / root.total_tokens
            if progress - last_prog > prog_delta:
                last_prog = int(progress / prog_delta) * prog_delta
                log.info(f"[{root.path.name}] progress: {progress:.2%}")

        return translated_root

    def _recursive_translate(self, block: CodeBlock) -> TranslatedCodeBlock:
        translated_block = TranslatedCodeBlock.from_original(block, self.target_language)
        self._add_translation(translated_block)
        if not translated_block.translated:
            return translated_block

        for child in block.children:
            # Don't bother translating children if they aren't used
            if self.combiner.contains_child(translated_block.code, child):
                translated_block.children.append(self._recursive_translate(child))
            else:
                log.warning(f"Skipping {child.id} (not referenced in parent code)")

        return translated_block

    def _add_translation(self, block: TranslatedCodeBlock) -> None:
        if block.translated:
            return

        if block.original.code is None:
            block.translated = True
            return

        identifier = f"{block.original.path.name}:{block.id}"

        log.debug(f"[{identifier}] Translating...")
        log.debug(f"[{identifier}] Input code:\n{block.original.code}")
        prompt = self._prompt_engine.create(block.original)
        input_cost = COST_PER_MODEL[self.model]["input"] * prompt.tokens / 1000.0
        cost = 0.0
        retry_count = 0
        best_seen = None
        least_missing = None

        # Retry the request up to max_prompts times before failing
        for retry_count in range(self.max_prompts + 1):
            output = self._llm.predict_messages(prompt.prompt)
            tokens = self._llm.get_num_tokens(output.content)
            output_cost = COST_PER_MODEL[self.model]["output"] * tokens / 1000.0
            cost += input_cost + output_cost

            # Pass through content if output is expected to be text
            if "text" == self.target_language:
                best_seen = output.content
                break

            # Otherwise parse for code
            try:
                parsed_output = self.parser.parse(output.content)
            except ValueError:
                log.warning(f"[{identifier}] Failed to parse output")
                log.debug(f"[{identifier}] Failed output:\n{output.content}")
                continue

            if best_seen is None:
                best_seen = parsed_output

            if self._validate(block.original, parsed_output):
                best_seen = parsed_output
                break

            n_missing = self.combiner.count_missing(block.original, parsed_output)
            if least_missing is None or n_missing < least_missing:
                least_missing = n_missing
                best_seen = parsed_output
        else:
            if best_seen is None:
                error_msg = (
                    f"[{identifier}] Failed to parse output after "
                    f"{self.max_prompts} retries. Marking as untranslated."
                )
                log.warning(error_msg)
                return

            log.warning(f"[{identifier}] Output not complete")

        log.debug(f"[[{identifier}] Output code:\n{best_seen}")

        block.code = best_seen
        block.tokens = self._llm.get_num_tokens(best_seen)
        block.cost = cost
        block.retries = retry_count
        block.translated = True

    def _validate(self, input_block: CodeBlock, output_code: str) -> bool:
        missing_children = []
        for child in input_block.children:
            if not self.combiner.contains_child(output_code, child):
                missing_children.append(child.id)
        if missing_children:
            log.warning(f"Child placeholders not present in code: {missing_children}")
            log.debug(f"Code:\n{output_code}")
            return False
        return True

    def _save_to_file(self, block: CodeBlock) -> None:
        """Save a file to disk.

        Arguments:
            block: The file to save.
        """
        block.path.parent.mkdir(parents=True, exist_ok=True)
        block.path.write_text(block.code, encoding="utf-8")

    def _load_model(self) -> None:
        """Check that the model is valid."""
        if self.model not in VALID_MODELS:
            raise ValueError(
                f"Invalid model: {self.model}. Valid models are: {VALID_MODELS}"
            )
        if self.model in tuple(TOKEN_LIMITS.keys()):
            self._max_tokens = TOKEN_LIMITS[self.model]
        else:
            self._max_tokens = 4096
        arguments = deepcopy(MODEL_DEFAULT_ARGUMENTS[self.model])
        arguments.update(self.model_arguments)
        self._llm = MODEL_CONSTRUCTORS[self.model](**arguments)

    def _load_prompt_engine(self) -> None:
        """Load the prompt engine."""
        self._prompt_engine = PromptEngine(
            self._llm,
            self.model,
            self.source_language,
            self.target_language,
            self.target_version,
            self.prompt_template,
        )

    def _load_combiner(self) -> None:
        """Load the Combiner object."""
        # Ensure we can actually combine the output
        # With the current algorithm, combining requires the target language to be
        # included in LANGUAGES and have a "comment"
        if self.target_language not in list(LANGUAGES.keys()):
            message = (
                f"Target language '{self.target_language}' not implemented. "
                "Output will not be combined."
            )
            log.error(message)
            raise ValueError(message)
        self.combiner = Combiner(self.target_language)

    def _load_splitter(self) -> None:
        """Load the Splitter object."""
        if self.source_language in CUSTOM_SPLITTERS:
            if self.source_language == "mumps":
                self.splitter = MumpsSplitter(
                    max_tokens=self._max_tokens, model=self._llm
                )
        elif self.source_language in list(LANGUAGES.keys()):
            self.splitter = TreeSitterSplitter(
                language=self.source_language,
                max_tokens=self._max_tokens,
                model=self._llm,
            )
        else:
            raise NotImplementedError(
                f"Source language '{self.source_language}' not implemented."
            )
        self._glob = f"**/*.{LANGUAGES[self.source_language]['suffix']}"

    def _load_parser(self) -> None:
        """Load the CodeParser Object"""
        self.parser = CodeParser(target_language=self.target_language)

    def _check_languages(self) -> None:
        """Check that the source and target languages are valid."""
        if self.source_language not in list(LANGUAGES.keys()):
            raise ValueError(
                f"Invalid source language: {self.source_language}. "
                "Valid source languages are found in `janus.utils.enums.LANGUAGES`."
            )
        if self.target_language not in list(LANGUAGES.keys()):
            raise ValueError(
                f"Invalid target language: {self.target_language}. "
                "Valid source languages are found in `janus.utils.enums.LANGUAGES`."
            )
