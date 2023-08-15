from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .language.block import CodeBlock, TranslatedCodeBlock
from .language.combine import TextCombiner
from .language.fortran import FortranSplitter
from .language.mumps import MumpsCombiner, MumpsSplitter
from .language.python import PythonCombiner
from .llm import (
    COST_PER_MODEL,
    MODEL_CONSTRUCTORS,
    MODEL_DEFAULT_ARGUMENTS,
    TOKEN_LIMITS,
)
from .parsers.code_parser import CodeParser
from .prompts.prompt import PromptEngine
from .utils.enums import (
    LANGUAGE_SUFFIXES,
    VALID_SOURCE_LANGUAGES,
    VALID_TARGET_LANGUAGES,
)
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
            prompt_template: name of prompt template (see PromptTemplate)
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
                prompt = self._prompt_engine.create(block)
                parsed = False
                num_tries = 0
                cost = COST_PER_MODEL[self.model]["input"] * prompt.tokens
                while not parsed:
                    # output, tokens, cost = self._llm.get_output(prompt.prompt)
                    output = self._llm.predict_messages(prompt.prompt)
                    if "text" == self.target_language:
                        parsed_output = output.content
                        parsed = True
                    else:
                        parsed_output, parsed = self._parse_llm_output(output.content)
                    if not parsed:
                        log.warning(
                            f"Failed to parse output for block in file {block.path.name}"
                        )

                    if num_tries > self.max_prompts:
                        log.error(
                            f"Failed to parse output after {num_tries} tries. Exiting."
                        )
                        raise RuntimeError(
                            f"Failed to parse output after {num_tries} tries. Exiting."
                        )
                    num_tries += 1
                tokens = self._llm.get_num_tokens(output.content)
                cost += COST_PER_MODEL[self.model]["output"] * tokens

                # Create the output file
                source_suffix = LANGUAGE_SUFFIXES[self.source_language]
                target_suffix = LANGUAGE_SUFFIXES[self.target_language]
                out_filename = file.path.name.replace(
                    f".{source_suffix}", f".{target_suffix}"
                )
                outpath = output_directory / out_filename
                out_block = self._output_to_block(
                    parsed_output, outpath, block, tokens, cost
                )
                out_blocks.append(out_block)

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
        """Unpack a code block into a list of `CodeBlocks`.

        Arguments:
            block: The code block to unpack.

        Returns:
            A list of code blocks.
        """
        blocks = [block]

        if block not in blocks:
            blocks.append(block)

        for child in block.children:
            blocks.extend(self._unpack_code_blocks(child))

        return blocks

    def _nest_code_blocks(self, blocks: List[CodeBlock]) -> CodeBlock:
        """Nest a list of code blocks.

        Arguments:
            blocks: The code blocks to nest.

        Returns:
            The top level code block.
        """
        return self._recurse_nest(blocks)[0]

    def _recurse_nest(self, blocks: List[CodeBlock]) -> List[CodeBlock]:
        """Recursively nest a list of code blocks.

        Arguments:
            blocks: The code blocks to nest.

        Returns:
            The nested code blocks.
        """
        result = []

        for code_block in blocks:
            depth = code_block.depth
            id = code_block.id

            children = [
                block for block in blocks if block.depth == depth + 1 and block.id == id
            ]

            code_block.children = self._recurse_nest(children)
            result.append(code_block)

        return result

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
        if self.target_language == "python":
            self.combiner = PythonCombiner()
        elif self.target_language == "mumps":
            self.combiner = MumpsCombiner()
        elif self.target_language == "text":
            self.combiner = TextCombiner()
        else:
            raise NotImplementedError(
                f"Target language '{self.target_language}' not implemented."
            )

    def _load_splitter(self) -> None:
        """Load the Splitter object."""
        if self.source_language == "fortran":
            self.splitter = FortranSplitter(max_tokens=self._max_tokens, model=self._llm)
            self._glob = "**/*.f90"
        elif self.source_language == "mumps":
            self.splitter = MumpsSplitter(max_tokens=self._max_tokens, model=self._llm)
            self._glob = "**/*.m"
        else:
            raise NotImplementedError(
                f"Source language '{self.source_language}' not implemented."
            )

    def _load_parser(self) -> None:
        """Load the CodeParser Object"""
        self.parser = CodeParser(target_language=self.target_language)

    def _check_languages(self) -> None:
        """Check that the source and target languages are valid."""
        if self.source_language not in VALID_SOURCE_LANGUAGES:
            raise ValueError(
                f"Invalid source language: {self.source_language}. "
                f"Valid source languages are: {VALID_SOURCE_LANGUAGES}"
            )
        if self.target_language not in VALID_TARGET_LANGUAGES:
            raise ValueError(
                f"Invalid target language: {self.target_language}. "
                f"Valid target languages are: {VALID_TARGET_LANGUAGES}"
            )
