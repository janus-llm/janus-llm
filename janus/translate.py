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
        use_placeholders: bool = True,
    ) -> None:
        """Initialize a Translator instance.

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set and the
                `OPENAI_ORG_ID` environment variable should be set if needed.
            source_language: The source programming language.
            target_language: The target programming language.
            target_version: The target version of the target programming language.
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
        self._load_splitter(use_placeholders=use_placeholders)
        self._load_combiner()
        self._load_prompt_engine()
        self._load_parser()

    def translate(
        self,
        input_directory: str | Path,
        output_directory: str | Path,
        overwrite: bool = False,
    ) -> None:
        """Translate code in the input directory from the source language to the target
        language, and write the resulting files to the output directory.

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

        target_suffix = LANGUAGES[self.target_language]["suffix"]

        input_paths = input_directory.glob(self._glob)

        # Now, loop through every code block in every file and translate it with an LLM
        total_cost = 0.0
        for in_path in input_paths:
            out_path = output_directory / in_path.with_suffix(f".{target_suffix}").name
            if out_path.exists() and not overwrite:
                continue

            out_block = self.translate_file(in_path)
            total_cost += out_block.total_cost

            # Don't attempt to write files for which translation failed
            if not out_block.translated:
                continue

            # Make sure the tree's code has been consolidated at the top level
            #  before writing to file
            self.combiner.combine(out_block)
            self._save_to_file(out_block, out_path)

        log.info(f"Total cost: ${total_cost:,.2f}")

    def translate_file(self, file: Path) -> TranslatedCodeBlock:
        """Translate a single file.

        Arguments:
            file: Input path to file

        Returns:
            A `TranslatedCodeBlock` object. This block does not have a path set, and its
            code is not guaranteed to be consolidated. To amend this, run
            `Combiner.combine_childen` on the block.
        """
        filename = file.name
        log.info(f"[{filename}] Splitting file")
        input_block = self.splitter.split(file)
        log.info(
            f"[{filename}] File split into {input_block.n_descendents:,} blocks, "
            f"tree of height {input_block.height}"
        )
        output_block = self._iterative_translate(input_block)
        if output_block.translated:
            completeness = output_block.translation_completeness
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
        """Translate the passed CodeBlock representing a full file.

        Arguments:
            root: A root block representing the top-level block of a file

        Returns:
            A `TranslatedCodeBlock`
        """
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
                if self.combiner.contains_child(translated_block.text, child):
                    translated_child = TranslatedCodeBlock.from_original(
                        child, self.target_language
                    )
                    translated_block.children.append(translated_child)
                    stack.append(translated_child)
                else:
                    log.warning(f"Skipping {child.id} (not referenced in parent code)")

            progress = translated_root.translation_completeness
            if progress - last_prog > prog_delta:
                last_prog = int(progress / prog_delta) * prog_delta
                log.info(f"[{root.name}] progress: {progress:.2%}")

        return translated_root

    def _recursive_translate(self, block: CodeBlock) -> TranslatedCodeBlock:
        """Recuresively translate the passed CodeBlock.

        Arguments:
            block: A `CodeBlock` to translate (may be a child in a larger tree)

        Returns:
            A `TranslatedCodeBlock`
        """
        translated_block = TranslatedCodeBlock.from_original(block, self.target_language)
        self._add_translation(translated_block)
        if not translated_block.translated:
            return translated_block

        for child in block.children:
            # Don't bother translating children if they aren't used
            if self.combiner.contains_child(translated_block.text, child):
                translated_block.children.append(self._recursive_translate(child))
            else:
                log.warning(f"Skipping {child.id} (not referenced in parent code)")

        return translated_block

    def _add_translation(self, block: TranslatedCodeBlock) -> None:
        """Given an "empty" `TranslatedCodeBlock`, translate the code represented in
        `block.original`, setting the relevant fields in the translated block. The
        `TranslatedCodeBlock` is updated in-pace, nothing is returned. Note that this
        translates *only* the code for this block, not its children.

        Arguments:
            block: An empty `TranslatedCodeBlock`
        """
        if block.translated:
            return

        if block.original.text is None:
            block.translated = True
            return

        identifier = block.name

        log.debug(f"[{identifier}] Translating...")
        log.debug(f"[{identifier}] Input text:\n{block.original.text}")
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
                block.retries = retry_count
                block.cost = cost
                return

            log.warning(f"[{identifier}] Output not complete")

        log.debug(f"[{identifier}] Output code:\n{best_seen}")

        block.text = best_seen
        block.tokens = self._llm.get_num_tokens(best_seen)
        block.cost = cost
        block.retries = retry_count
        block.translated = True

    def _validate(self, input_block: CodeBlock, output_code: str) -> bool:
        """Validate the given output code by ensuring it contains all necessary
        placeholders corresponding to the children of the given input block

        Arguments:
            input_block: A `CodeBlock` representing the input to the LLM
            output_code: The parsed code returned by the LLM

        Returns:
            Whether the given code is valid; `True` if all the child blocks are
            referenced, `False` otherwise.
        """
        missing_children = []
        for child in input_block.children:
            if not self.combiner.contains_child(output_code, child):
                missing_children.append(child.id)
        if missing_children:
            log.warning(
                f"[{input_block.name}] Child placeholders not present in text: "
                f"{missing_children}"
            )
            log.debug(f"Code:\n{output_code}")
            return False
        return True

    def _save_to_file(self, block: CodeBlock, out_path: Path) -> None:
        """Save a file to disk.

        Arguments:
            block: The `CodeBlock` to save to a file.
        """
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(block.text, encoding="utf-8")

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
        """Load the `Combiner` object."""
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

    def _load_splitter(self, use_placeholders: bool = True) -> None:
        """Load the `Splitter` object."""
        if self.source_language in CUSTOM_SPLITTERS:
            if self.source_language == "mumps":
                self.splitter = MumpsSplitter(
                    max_tokens=self._max_tokens,
                    model=self._llm,
                )
        elif self.source_language in list(LANGUAGES.keys()):
            self.splitter = TreeSitterSplitter(
                language=self.source_language,
                max_tokens=self._max_tokens,
                model=self._llm,
                use_placeholders=use_placeholders,
            )
        else:
            raise NotImplementedError(
                f"Source language '{self.source_language}' not implemented."
            )
        self._glob = f"**/*.{LANGUAGES[self.source_language]['suffix']}"

    def _load_parser(self) -> None:
        """Load the `CodeParser` Object"""
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
