import os
from pathlib import Path

from langchain.schema.language_model import BaseLanguageModel

from ...utils.enums import LANGUAGES
from ...utils.logger import create_logger
from ..splitter import Splitter

log = create_logger(__name__)

tree_sitter_build_dir = os.environ.get("TREE_SITTER_BUILD_DIR")

if tree_sitter_build_dir is None:
    TREE_SITTER_BUILD_DIR: Path = Path.home() / ".janus/tree-sitter/build-files"
else:
    TREE_SITTER_BUILD_DIR: Path = Path(tree_sitter_build_dir)


class TreeSitterSplitter(Splitter):
    """A class for splitting all tree-sitter language code into functional blocks to
    prompt for transcoding.
    """

    def __init__(
        self, language: str, model: BaseLanguageModel, max_tokens: int = 4096
    ) -> None:
        """Initialize a TreeSitterSplitter instance.

        Arguments:
            language: The name of the language to split.
            model: The name of the model to use for translation.
            max_tokens: The maximum number of tokens to use for each functional block.
        """
        super().__init__(language, model, max_tokens)
        url = LANGUAGES[self.language]["url"]
        if url is None:
            message = f"Tree-sitter does not support {self.language} yet."
            log.error(message)
            raise ValueError(message)
        self._load_parser(TREE_SITTER_BUILD_DIR, url)
