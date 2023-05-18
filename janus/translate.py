import os
from pathlib import Path
from typing import Dict, List, Tuple

from .language.block import File
from .language.fortran import FortranSplitter
from .llm.openai import TOKEN_LIMITS, OpenAI

VALID_SOURCE_LANGUAGES: Tuple[str, ...] = ("fortran",)
VALID_TARGET_LANGUAGES: Tuple[str, ...] = ("python",)
VALID_MODELS: Tuple[str, ...] = tuple(TOKEN_LIMITS.keys())

LANGUAGE_SUFFIXES: Dict[str, str] = {
    "fortran": "f90",
    "python": "py",
}


class Translator:
    """A class that translates code from one programming language to another."""

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        source_language: str = "fortran",
        target_language: str = "python",
    ) -> None:
        """Initialize a Translator instance.

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                   `OPENAI_API_KEY` environment variable must be set and the
                   `OPENAI_ORG_ID` environment variable should be set if needed.
            source_language: The source programming language.
            target_language: The target programming language.
        """
        self.model = model
        self.source_language = source_language.lower()
        self.target_language = target_language.lower()
        self._check_languages()
        self._load_model()

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

        # Now, loop through every code block in every file and translate it with an LLM
        for file in files:
            pass

    def _get_files(self, directory: Path) -> List[File]:
        """Get the files in the given directory and split them into functional blocks.

        Arguments:
            directory: The directory to get the files from.

        Returns:
            A list of `File`s.
        """
        if self.source_language == "fortran":
            splitter = FortranSplitter()
            glob = "**/*.f90"
        else:
            raise NotImplementedError(
                f"Source language '{self.source_language}' not implemented."
            )

        files: List[File] = []

        for file in Path(directory).glob(glob):
            files.append(splitter.split(file))

        return files

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
