import os
import re
from pathlib import Path
from typing import List, Tuple

from .language.block import CodeBlock, File, TranslatedCodeBlock
from .language.fortran import FortranSplitter
from .llm.openai import TOKEN_LIMITS, OpenAI
from .prompts.prompt import PromptEngine
from .utils.enums import (
    LANGUAGE_SUFFIXES,
    VALID_SOURCE_LANGUAGES,
    VALID_TARGET_LANGUAGES,
)
from .utils.logger import create_logger

log = create_logger(__name__)

VALID_MODELS: Tuple[str, ...] = tuple(TOKEN_LIMITS.keys())


class Translator:
    """A class that translates code from one programming language to another."""

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        source_language: str = "fortran",
        target_language: str = "python",
        target_version: str = "3.10",
    ) -> None:
        """Initialize a Translator instance.

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                   `OPENAI_API_KEY` environment variable must be set and the
                   `OPENAI_ORG_ID` environment variable should be set if needed.
            source_language: The source programming language.
            target_language: The target programming language.
        """
        self.model = model.lower()
        self.source_language = source_language.lower()
        self.target_language = target_language.lower()
        self.target_version = target_version
        self._check_languages()
        self._load_model()
        self._load_prompt_engine()

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

        translated_files: List[File] = []

        # Now, loop through every code block in every file and translate it with an LLM
        for file in files:
            out_blocks: List[TranslatedCodeBlock] = []
            # Loop through all code blocks in the file
            for code in file.blocks:
                prompt = self._prompt_engine.create(code)
                output, tokens, cost = self._llm.get_output(prompt.prompt)
                log.debug(f"Block {code.block_id} in {file.path.name}: {output}")
                parsed_output, parsed = self._parse_llm_output(output)
                if not parsed:
                    log.warning(
                        f"Failed to parse output for block {code.block_id} in file "
                        f"{file.path.name}"
                    )

                # Create the output file
                source_suffix = LANGUAGE_SUFFIXES[self.source_language]
                target_suffix = LANGUAGE_SUFFIXES[self.target_language]
                out_filename = file.path.name.replace(
                    f".{source_suffix}", f".{target_suffix}"
                )
                outpath = output_directory / out_filename
                out_blocks.append(
                    self._output_to_block(parsed_output, outpath, code, tokens, cost)
                )
            # Write the code blocks to the output file
            outfile = File(outpath, out_blocks)
            self._save_to_file(outfile)
            # Add the translated file to the list of translated files
            translated_files.append(outfile)

        self.output_files = translated_files

    def _save_to_file(self, file: File) -> None:
        """Save a file to disk.

        Arguments:
            file: The file to save.
        """
        file.path.parent.mkdir(parents=True, exist_ok=True)
        with open(file.path, "w") as f:
            f.writelines([f"{b.code}\n" for b in file.blocks])

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
            output,
            outpath,
            original_block.complete,
            original_block.block_id,
            original_block.segment_id,
            self.target_language,
            "",
            tokens["completion_tokens"],
            original_block,
            cost,
        )
        return block

    def _get_files(self, directory: Path) -> List[File]:
        """Get the files in the given directory and split them into functional blocks.

        Arguments:
            directory: The directory to get the files from.

        Returns:
            A list of `File`s.
        """
        if self.source_language == "fortran":
            splitter = FortranSplitter(max_tokens=self._llm.model_max_tokens)
            glob = "**/*.f90"
        else:
            raise NotImplementedError(
                f"Source language '{self.source_language}' not implemented."
            )

        files: List[File] = []

        for file in Path(directory).glob(glob):
            files.append(splitter.split(file))

        return files

    def _parse_llm_output(self, output: str) -> Tuple[str, bool]:
        """Parse the output of an LLM.

        Arguments:
            output: The output of the LLM.

        Returns:
            The parsed output.
        """
        pattern = rf"```[^\S\r\n]*(?:{self.target_language}[^\S\r\n]*)?\n?(.*?)\n*```"
        try:
            response = re.search(pattern, output, re.DOTALL).group(1)
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
        self._llm = OpenAI(
            self.model, os.getenv("OPENAI_API_KEY"), os.getenv("OPENAI_ORG_ID")
        )

    def _load_prompt_engine(self) -> None:
        """Load the prompt engine."""
        self._prompt_engine = PromptEngine(
            self.model,
            self.source_language,
            self.target_language,
            self.target_version,
            "simple",
        )

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
