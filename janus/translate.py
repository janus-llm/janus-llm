from copy import deepcopy
from pathlib import Path
from collections import defaultdict
from typing import Any, Dict, List, Tuple, Optional

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

        # First, get the files in the input directory and split them into CodeBlocks
        input_files = (
            self.splitter.split(file)
            for file in input_directory.glob(self._glob)
        )
        translated_files = map(self._recursive_translate, input_files)

        # Now, loop through every code block in every file and translate it with an LLM
        total_cost = 0.0
        for out_block in translated_files:
            # Create the output file
            out_block.path = output_directory / out_block.original.path.name.replace(
                f".{source_suffix}",
                f".{target_suffix}"
            )

            self.combiner.combine_children(out_block)
            file_cost = 0
            stack = [out_block]
            while stack:
                node = stack.pop()
                file_cost += node.cost
                stack.extend(node.children)
            log.info(f"Total cost for {out_block.original.path.name}: ${file_cost:,.2f}")
            total_cost += file_cost

            # Write the code blocks to the output file
            self._save_to_file(out_block)

        log.info(f"Total cost: ${total_cost:,.2f}")

    def _recursive_translate(self, block: CodeBlock) -> TranslatedCodeBlock:
        translated_block = TranslatedCodeBlock.from_original(block, self.target_language)

        if block.code is not None:
            translated_code, cost = self._translate_block(block)
            translated_block.code = translated_code
            translated_block.cost = cost

        for child in block.children:
            # Don't bother translating children if they aren't used
            if self.combiner.contains_child(translated_block.code, child):
                translated_block.children.append(self._recursive_translate(child))
            else:
                log.warning(f"Skipping {child.id} (not referenced in parent code)")

        return translated_block

    def _translate_block(self, block: CodeBlock) -> Tuple[str, float]:
        log.debug(f"Input code ({block.path.name}, {block.id}):\n{block.code}")
        prompt = self._prompt_engine.create(block)
        input_cost = COST_PER_MODEL[self.model]["input"] * prompt.tokens / 1000.
        cost = 0.0
        parsed_output = None

        # Retry the request up to max_prompts times before failing
        for retry_count in range(self.max_prompts + 1):
            if retry_count:
                log.warning(f"Retry number {retry_count}")
            output = self._llm.predict_messages(prompt.prompt)
            tokens = self._llm.get_num_tokens(output.content)
            output_cost = COST_PER_MODEL[self.model]["output"] * tokens / 1000.
            cost += input_cost + output_cost

            # Pass through content if output is expected to be text
            if "text" == self.target_language:
                parsed_output = output.content
                break

            # Otherwise parse for code
            try:
                parsed_output = self.parser.parse(output.content)
            except ValueError:
                log.warning(f"Failed to parse output for block in file {block.path.name}")
                log.debug(f"Failed output:\n{output.content}")
                continue

            valid = self.combiner.validate(parsed_output, block)
            if valid:
                break
        else:
            if parsed_output is None:
                error_msg = (
                    f"Failed to parse output for block in file "
                    f"{block.path.name} after {self.max_prompts} retries."
                )
                log.error(error_msg)
                raise RuntimeError(error_msg)

            log.warning(f"Output for block {block.id} not valid")

        log.debug(f"Output code ({block.path.name}, {block.id}):\n{parsed_output}")
        return parsed_output, cost

    def _save_to_file(self, block: CodeBlock) -> None:
        """Save a file to disk.

        Arguments:
            block: The file to save.
        """
        block.path.parent.mkdir(parents=True, exist_ok=True)
        block.path.write_text(block.code, encoding="utf-8")

    def _get_files(self, directory: Path) -> List[CodeBlock]:
        """Get the files in the given directory and split them into functional blocks.

        Arguments:
            directory: The directory to get the files from.

        Returns:
            A list of code blocks.
        """
        files: List[CodeBlock] = []

        for file in Path(directory).glob(self._glob):
            files.append(self.splitter.split(file))

        return files

    def _unpack_code_blocks(self, block: CodeBlock) -> List[CodeBlock]:
        """Unpack a code block into a list of `CodeBlocks`. List order is
            top-down, depth first.

        Arguments:
            block: The code block to unpack.

        Returns:
            A list of code blocks.
        """
        return sum(map(self._unpack_code_blocks, block.children), [block])

    def _nest_code_blocks(self, blocks: List[CodeBlock]) -> CodeBlock:
        """Nest a depth-first list of code blocks. The root should be the first
            block in the list.

        Arguments:
            blocks: The code blocks to nest.

        Returns:
            The top level code block.
        """
        id_to_children = defaultdict(list)
        for block in blocks:
            id_to_children[block.parent_id].append(block)
        for block in blocks:
            block.children = id_to_children[block.id]
        return blocks[0]

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
