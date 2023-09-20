import platform
import os
from pathlib import Path

import tree_sitter
from git import Repo
from langchain.schema.language_model import BaseLanguageModel

from ...utils.enums import LANGUAGES
from ...utils.logger import create_logger
from ..splitter import Splitter
from ..node import ASTNode

log = create_logger(__name__)


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
        self._load_parser()

    def _get_ast(self, code: str | bytes) -> ASTNode:
        if isinstance(code, str):
            code = bytes(code, "utf-8")

        tree = self.parser.parse(code)
        cursor = tree.walk()
        root = ASTNode.from_tree_sitter_node(cursor.node, code)
        return root

    def _load_parser(self) -> None:
        """Load the parser for the given language.

        Sets `self.parser`'s language to the one specified in `self.language`.

        Arguments:
            build_dir: The directory to store the so file in.
            github_url: The url to the tree-sitter GitHub repository for the language.
        """
        # Get the directory to store the file in from environment (or default)
        build_dir: Path = Path.home() / ".janus/tree-sitter/build-files"
        if (custom_dir := os.environ.get("TREE_SITTER_BUILD_DIR")) is not None:
            build_dir = Path(custom_dir)

        # Locate the .so file, generate the file if necessary
        platform_str = f"{platform.system()}_{platform.processor()}"
        so_file = build_dir / f"{self.language}_parser_{platform_str}.so"
        if not so_file.exists():
            log.warning(
                f"Could not load {so_file}, building one for {platform.system()} "
                f"system, with {platform.processor()} processor"
            )
            self._create_parser(so_file)

        # Load the parser using the generated .so file
        self.parser: tree_sitter.Parser = tree_sitter.Parser()
        self.parser.set_language(tree_sitter.Language(so_file, self.language))

    def _create_parser(self, so_file: Path | str) -> None:
        """Create the parser for the given language.

        Arguments:
            so_file: The path to the so file for the language.
        """
        # Store the library in the `build` directory
        tree_sitter_dir = Path.home() / ".tree-sitter"
        tree_sitter_dir.mkdir(exist_ok=True)
        lang_dir = tree_sitter_dir / f"tree-sitter-{self.language}"

        if not lang_dir.exists():
            github_url = LANGUAGES[self.language]["url"]
            if github_url is None:
                message = f"Tree-sitter does not support {self.language} yet."
                log.error(message)
                raise ValueError(message)
            self._git_clone(github_url, lang_dir)

        tree_sitter.Language.build_library(str(so_file), [str(lang_dir)])

    @staticmethod
    def _git_clone(repository_url: str, destination_folder: Path | str) -> None:
        try:
            Repo.clone_from(repository_url, destination_folder)
            log.debug(f"{repository_url} cloned to {destination_folder}")
        except Exception as e:
            log.error(f"Error: {e}")
            raise e