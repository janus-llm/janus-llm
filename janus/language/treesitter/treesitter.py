import os
import platform
import subprocess
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
        skip_merge: bool = False,
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
            skip_merge=skip_merge,
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

        # Convert to string for ctypes
        so_file_str = str(so_file)

        # Load the parser using the generated .so file
        pointer = self._so_to_pointer(so_file_str)
        lang = tree_sitter.Language(pointer)
        self.parser: tree_sitter.Parser = tree_sitter.Parser(lang)

    def _so_to_pointer(self, so_file: str) -> int:
        """Convert the .so file to a pointer.

        Taken from `treesitter.Language.__init__` to get past deprecated warning.

        Arguments:
            so_file: The path to the .so file for the language.

        Returns:
            The pointer to the language.
        """
        lib = cdll.LoadLibrary(os.fspath(so_file))
        # Handle case where grammar authors have uppercase vs. lowercase name
        try:
            if self.language == "binary":
                # Special case for binary, which uses the c parser
                language_function = getattr(lib, "tree_sitter_c")
            else:
                language_function = getattr(lib, f"tree_sitter_{self.language}")
        except AttributeError:
            language = self.language.upper()
            language_function = getattr(lib, f"tree_sitter_{language}")

        language_function.restype = c_void_p
        pointer = language_function()
        return pointer

    def _create_parser(self, so_file: Path | str) -> None:
        """Create the parser for the given language by:
           1. Cloning the grammar repo (if needed)
           2. Running `tree-sitter generate` in that repo
           3. Compiling only the C sources under `src/` into a shared library

        Arguments:
            so_file: The path to the .so file to produce.
        """
        # 1) Ensure the .so directory exists
        so_file_path = Path(so_file)
        so_file_path.parent.mkdir(parents=True, exist_ok=True)

        # 2) Clone (or update) the grammar repository
        tree_sitter_dir = Path.home() / ".tree-sitter"
        tree_sitter_dir.mkdir(exist_ok=True)
        if self.language == "binary":
            # Special case for binary, which uses the c parser
            lang_dir = tree_sitter_dir / "tree-sitter-c"
        else:
            lang_dir = tree_sitter_dir / f"tree-sitter-{self.language}"

        if not lang_dir.exists():
            github_url = LANGUAGES[self.language]["url"]
            if github_url is None:
                message = f"Tree-sitter does not support {self.language} yet."
                log.error(message)
                raise ValueError(message)

            try:
                if LANGUAGES[self.language].get("branch"):
                    self._git_clone(
                        github_url, lang_dir, LANGUAGES[self.language]["branch"]
                    )
                else:
                    self._git_clone(github_url, lang_dir)
            except Exception as e:
                raise RuntimeError(f"Could not clone {github_url}: {e}")

        # 3) Run `tree-sitter generate` inside the grammar directory to produce parser.c,
        # scanner.c, etc.
        try:
            # This assumes `tree-sitter` CLI is on PATH
            subprocess.run(
                ["tree-sitter", "generate"],
                cwd=str(lang_dir),
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )  # nosec: B603, B607
        except FileNotFoundError:
            raise RuntimeError(
                "Could not find `tree-sitter` CLI. Please install it and ensure it's on "
                "your PATH."
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(
                f"Error running `tree-sitter generate` in {lang_dir}:\n"
                f"{e.stderr.decode().strip()}"
            )

        # 4) Collect only the .c files under 'src/' (to avoid binding.c or other extras).
        src_dir = lang_dir / "src"
        if not src_dir.exists():
            raise RuntimeError(f"No `src/` directory found in {lang_dir} after generate.")
        c_files = list(src_dir.rglob("*.c"))
        if not c_files:
            raise RuntimeError(f"No C source files found under {src_dir} after generate.")

        # 5) Compile them into a shared object.
        #
        #    - We assume a POSIX-like compiler (gcc/cc) that accepts:
        #       cc -O3 -shared -fPIC -o <so_file> <all .c> -I<src_dir>
        #
        include_flags = [f"-I{src_dir}"]
        compile_cmd = [
            "cc",
            "-O3",
            "-shared",
            "-fPIC",
            "-Wno-error=implicit-function-declaration",
            "-o",
            str(so_file_path),
        ]
        compile_cmd += include_flags + [str(c_path) for c_path in c_files]

        try:
            subprocess.run(
                compile_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )  # nosec: B603
        except FileNotFoundError:
            raise RuntimeError(
                "Could not find a C compiler (`cc`). Please install `gcc` or similar."
            )
        except subprocess.CalledProcessError as e:
            stderr = e.stderr.decode().strip()
            raise RuntimeError(
                f"Error compiling C sources for {self.language}:\n{stderr}"
            )

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
