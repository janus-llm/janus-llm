from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Tuple

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

        # First, get the files in the input directory and split them into CodeBlocks
        files = self._get_files(input_directory)

        translated_files: List[TranslatedCodeBlock] = []

        # Now, loop through every code block in every file and translate it with an LLM
        for file in files:
            # out_blocks is flat, whereas `translated_files` is nested
            out_blocks: List[TranslatedCodeBlock] = []
            # Loop through all code blocks in the file
            blocks = self._unpack_code_blocks(file)
            for block in blocks:
                log.debug(f"Input code ({block.path.name}, {block.id}):\n{block.code}")
                prompt = self._prompt_engine.create(block)
                cost = COST_PER_MODEL[self.model]["input"] * prompt.tokens

                # Retry the request up to max_prompts times before failing
                for _ in range(self.max_prompts + 1):
                    output = self._llm.predict_messages(prompt.prompt)
                    if "text" == self.target_language:
                        # Pass through content if output is expected to be text
                        parsed_output = output.content
                        break

                    # Otherwise parse for code
                    parsed_output, parsed = self._parse_llm_output(output.content)
                    if not parsed:
                        log.warning(f"Failed to parse output for block in file {block.path.name}")
                        log.debug(f"Failed output:\n{parsed_output}")
                        continue

                    valid = self.combiner.validate(parsed_output, block)
                    if not valid:
                        continue

                    break
                else:
                    error_msg = (
                        f"Failed to parse output for block in file "
                        f"{block.path.name} after {self.max_prompts} retries."
                    )
                    log.error(error_msg)
                    raise RuntimeError(error_msg)

                tokens = self._llm.get_num_tokens(output.content)
                cost += COST_PER_MODEL[self.model]["output"] * tokens

                # Create the output file
                source_suffix = LANGUAGES[self.source_language]["suffix"]
                target_suffix = LANGUAGES[self.target_language]["suffix"]
                out_filename = file.path.name.replace(
                    f".{source_suffix}", f".{target_suffix}"
                )
                outpath = output_directory / out_filename
                out_block = self._output_to_block(
                    parsed_output, outpath, block, tokens, cost
                )
                log.debug(f"Output code ({out_block.path.name}, {out_block.id}):\n{out_block.code}")
                out_blocks.append(out_block)

            # The first block is the root
            out_file = self._nest_code_blocks(out_blocks)

            # Write the code blocks to the output file
            self._save_to_file(out_file)
            # Add the translated file to the list of translated files
            translated_files.append(out_file)

        self.output_files = translated_files

    def _save_to_file(self, file: CodeBlock) -> None:
        """Save a file to disk.

        Arguments:
            file: The file to save.
        """
        file.path.parent.mkdir(parents=True, exist_ok=True)
        self.combiner.blocks_to_file(file)

    def _output_to_block(
        self,
        output: str,
        outpath: Path,
        original_block: CodeBlock,
        tokens: int,
        cost: float,
    ) -> TranslatedCodeBlock:
        """Convert the output of an LLM to a `TranslatedCodeBlock`.

        Arguments:
            output: The output of the LLM.

        Returns:
            A `TranslatedCodeBlock` instance.
        """
        block = TranslatedCodeBlock(
            code=output,
            path=outpath,
            complete=original_block.complete,
            start_line=original_block.start_line,
            end_line=original_block.end_line,
            depth=original_block.depth,
            id=original_block.id,
            parent_id=original_block.parent_id,
            language=self.target_language,
            type=original_block.type,
            tokens=tokens,
            children=[],
            original=original_block,
            cost=cost,
        )
        return block

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
        for parent_block in blocks:
            parent_block.children = [
                block for block in blocks if block.parent_id == parent_block.id
            ]
        return blocks[0]

    def _parse_llm_output(self, output: str) -> Tuple[str, bool]:
        """Parse the output of an LLM.

        Arguments:
            output: The output of the LLM.

        Returns:
            The parsed output.
        """
        try:
            response = self.parser.parse(output)
            parsed = True
        except Exception:
            log.warning(f"Could not find code in output:\n\n{output}")
            response = output
            parsed = False

        return response, parsed

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
