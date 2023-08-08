from pathlib import Path

from ...utils.logger import create_logger
from ..splitter import Splitter
from langchain.schema.language_model import BaseLanguageModel

TREE_SITTER_FORTRAN_BUILD_DIR: Path = Path("janus/language/fortran/build_files")
TREE_SITTER_GITHUB_LINK: str = "https://github.com/stadelmanma/tree-sitter-fortran.git"

log = create_logger(__name__)


class FortranSplitter(Splitter):
    """A class for splitting Fortran code into functional blocks to prompt for
       transcoding.

    Attributes:
        patterns: A tuple of `Pattern`s to use for splitting Fortran code into
                  functional blocks.
        max_tokens: The maximum number of tokens to use for each functional block.
    """

    def __init__(self, model: BaseLanguageModel, max_tokens: int = 4096) -> None:
        """Initialize a FortranSplitter instance.

        Arguments:
            max_tokens: The maximum number of tokens to use for each functional block.
            model: The name of the model to use for translation.
        """
        self.language: str = "fortran"
        super().__init__(model, max_tokens)
        self._load_parser(TREE_SITTER_FORTRAN_BUILD_DIR, TREE_SITTER_GITHUB_LINK)
