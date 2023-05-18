import os
import re
from pathlib import Path
from typing import List, Tuple

from .language.block import CodeBlock, File, TranslatedCodeBlock
from .language.fortran import FortranSplitter
from .llm.openai import TOKEN_LIMITS, OpenAI
from .prompts.prompt import PromptEngine
from .utils.logger import create_logger

log = create_logger(__name__)

VALID_SOURCE_LANGUAGES: Tuple[str, ...] = ("fortran",)
VALID_TARGET_LANGUAGES: Tuple[str, ...] = ("python",)
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
        # First, get the files in the input directory and split them into CodeBlocks
        files = self._get_files(input_directory)

        translated_files: List[File] = []

        # Now, loop through every code block in every file and translate it with an LLM
        for file in files:
            blocks: List[TranslatedCodeBlock] = []
            for code in file.blocks:
                prompt = self._prompt_engine.create(code)
                output, tokens, cost = self._llm.get_output(prompt.prompt)
                parsed_output = self._parse_llm_output(output)
                # TODO: Where I'm currently devving
                new_filename = file.path.name.replace(".f90", ".py")
                outpath = Path(output_directory) / new_filename
                blocks.append(
                    self._output_to_block(parsed_output, outpath, code, tokens, cost)
                )
            translated_files.append(File(file.path, blocks))

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

    def _parse_llm_output(self, output: str) -> str:
        """Parse the output of an LLM.

        Arguments:
            output: The output of the LLM.

        Returns:
            The parsed output.
        """
        try:
            # response = re.findall(r"\{.*?\}", output)[0].strip("{}")
            pattern = r"```(.*?)```"
            response = re.search(pattern, output, re.DOTALL)
            response = response.group(1).strip("python\n")
        except Exception:
            log.warning(f"Could not find code in output:\n\n{output}")

        return response

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
