import os
import platform
from collections import defaultdict
from ctypes import c_void_p, cdll
from pathlib import Path
from typing import Optional

import tree_sitter
from git import Repo

from janus.language.block import CodeBlock, NodeType
from janus.language.splitter import Splitter
from janus.llm.models_info import JanusModel
from janus.utils.enums import LANGUAGES
from janus.utils.logger import create_logger

log = create_logger(__name__)


class TreeSitterSplitter(Splitter):
    """A class for splitting all tree-sitter language code into functional blocks to
    prompt for transcoding.
    """

    def __init__(
        self,
        language: str,
        model: JanusModel | None = None,
        max_tokens: int = 4096,
        protected_node_types: tuple[str, ...] = (),
        prune_node_types: tuple[str, ...] = (),
        prune_unprotected: bool = False,
    ) -> None:
        """Initialize a TreeSitterSplitter instance.

        Arguments:
            language: The name of the language to split.
            model: The name of the model to use for translation.
            max_tokens: The maximum number of tokens to use for each functional block.
        """
        super().__init__(
            language=language,
            model=model,
            max_tokens=max_tokens,
            protected_node_types=protected_node_types,
            prune_node_types=prune_node_types,
            prune_unprotected=prune_unprotected,
        )
        self._load_parser()

    def _get_ast(self, code: str) -> CodeBlock:
        code_bytes = bytes(code, "utf-8")
        tree = self.parser.parse(code_bytes)
        root = tree.walk().node
        root = self._node_to_block(root, code_bytes)
        return root

    # Recursively print tree to view parsed output (dev helper function)
    # Example call: self._print_tree(tree.walk(), "")
    def _print_tree(self, cursor: tree_sitter.TreeCursor, indent: str) -> None:
        node = cursor.node
        print(f"{indent}{node.type} {node.start_point}-{node.end_point}")
        if cursor.goto_first_child():
            while True:
                self._print_tree(cursor, indent + "    ")
                if not cursor.goto_next_sibling():
                    break
            cursor.goto_parent()

    def _set_identifiers(self, root: CodeBlock, name: str):
        seen_types = defaultdict(int)
        queue = [root]
        while queue:
            node = queue.pop(0)  # BFS order to keep lower IDs toward the root
            node.id = f"{node.node_type}[{seen_types[node.node_type]}]"
            seen_types[node.node_type] += 1
            node.name = f"{name}:{node.id}"
            queue.extend(node.children)

    def _node_to_block(self, node: tree_sitter.Node, original_text: bytes) -> CodeBlock:
        """Convert a tree_sitter Node into a CodeBlock. The original text is
        used to populate the prefix and suffix of the node. This function is
        recursively called for all children of the node.

        """
        prefix_start = 0
        if node.prev_sibling is not None:
            prefix_start = node.prev_sibling.end_byte
        elif node.parent is not None:
            prefix_start = node.parent.start_byte
        prefix = original_text[prefix_start : node.start_byte].decode()

        suffix_end = len(original_text)
        if node.next_sibling is not None:
            suffix_end = node.next_sibling.start_byte
        elif node.parent is not None:
            suffix_end = node.parent.end_byte
        suffix = original_text[node.end_byte : suffix_end].decode()

        text = node.text.decode()
        children = [self._node_to_block(child, original_text) for child in node.children]
        return CodeBlock(
            id=node.id,
            name=str(node.id),
            text=text,
            affixes=(prefix, suffix),
            start_point=node.start_point,
            end_point=node.end_point,
            start_byte=node.start_byte,
            end_byte=node.end_byte,
            node_type=NodeType(node.type),
            children=children,
            language=self.language,
            tokens=self._count_tokens(text),
        )

    def _load_parser(self) -> None:
        """Load the parser for the given language.

        Sets `self.parser`'s language to the one specified in `self.language`.
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

        # string required for Windows, as 'WindowsPath' is not iterable
        so_file = str(so_file)

        # Load the parser using the generated .so file
        self.parser: tree_sitter.Parser = tree_sitter.Parser()
        pointer = self._so_to_pointer(so_file)
        self.parser.set_language(tree_sitter.Language(pointer, self.language))

    def _so_to_pointer(self, so_file: str) -> int:
        """Convert the .so file to a pointer.

        Taken from `treesitter.Language.__init__` to get past deprecated warning.

        Arguments:
            so_file: The path to the so file for the language.

        Returns:
            The pointer to the language.
        """
        lib = cdll.LoadLibrary(os.fspath(so_file))
        language_function = getattr(lib, f"tree_sitter_{self.language}")
        language_function.restype = c_void_p
        pointer = language_function()
        return pointer

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
            if LANGUAGES[self.language].get("branch"):
                self._git_clone(github_url, lang_dir, LANGUAGES[self.language]["branch"])
            else:
                self._git_clone(github_url, lang_dir)

        tree_sitter.Language.build_library(str(so_file), [str(lang_dir)])

    @staticmethod
    def _git_clone(
        repository_url: str, destination_folder: Path | str, branch: Optional[str] = None
    ) -> None:
        try:
            if branch:
                Repo.clone_from(repository_url, destination_folder, branch=branch)
            else:
                Repo.clone_from(repository_url, destination_folder)
            log.debug(f"{repository_url} cloned to {destination_folder}")
        except Exception as e:
            log.error(f"Error: {e}")
            raise e
