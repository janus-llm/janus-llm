import platform
from pathlib import Path
from typing import Hashable, Optional, Callable

import tree_sitter
from git import Repo
from langchain.schema.language_model import BaseLanguageModel

from ..utils.logger import create_logger
from .block import CodeBlock
from .file import FileManager

log = create_logger(__name__)


class TokenLimitError(Exception):
    """An exception raised when the token limit is exceeded and the code cannot be
    split into smaller blocks.
    """

    pass


class Splitter(FileManager):
    """A class for splitting code into functional blocks to prompt with for
    transcoding.
    """

    def __init__(self, language: str, model: BaseLanguageModel, max_tokens: int = 4096):
        """
        Arguments:
            max_tokens: The maximum number of tokens to use for each functional block.
            model: The name of the model to use for translation.
        """
        super().__init__(language=language)
        # Divide max_tokens by 3 because we want to leave just as much space for the
        # prompt as for the translated code.
        self.max_tokens: int = max_tokens // 3
        self.parser: tree_sitter.Parser = tree_sitter.Parser()
        self.model = model

    def split(self, file: Path | str) -> CodeBlock:
        """Split the given file into functional code blocks.

        Arguments:
            file: The file to split into functional blocks.

        Returns:
            A `CodeBlock` made up of nested `CodeBlock`s.
        """
        path = Path(file)
        code = path.read_text()
        block = self._split(code, path)
        return block

    def _split(self, code: str | bytes, path: Path) -> CodeBlock:
        """Use tree-sitter to walk through the code and split into functional code blocks.

        The functional code blocks will have children if each individual code block
        doesn't fit within `self.max_tokens`.

        Arguments:
            code: The code to split up.
            path: The path to the file containing the code.

        Returns:
            A nested `CodeBlock`.
        """
        if isinstance(code, str):
            code = bytes(code, "utf-8")

        tree = self.parser.parse(code)
        cursor = tree.walk()

        seen_ids = set()
        def id_gen():
            block_id = f"<<<child_{len(seen_ids)}>>>"
            seen_ids.add(block_id)
            return block_id

        return self._recurse_split(
            node=cursor.node,
            path=path,
            depth=0,
            parent_id=None,
            id_gen=id_gen
        )

    def _recurse_split(
            self,
            node: tree_sitter.Node,
            path: Path,
            depth: int,
            parent_id: Optional[Hashable],
            id_gen: Callable[[], Hashable]
        ) -> CodeBlock:
        """Recursively split the code into functional blocks.

        Arguments:
            node: The current node in the tree.
            path: The path to the file containing the code.
            depth: The current depth of the recursion.
            parent_id: The id of the calling parent
            id_gen: A function with which to generate child ids

        Returns:
            A CodeBlock object.
        """
        # First get the text for all the siblings at this level
        text = node.text.decode()
        block_length = self._count_tokens(text)
        node_id = id_gen()

        # If the text at the function input is less than the max tokens, then
        #  we can just return it as a CodeBlock with no children.
        if self._count_tokens(text) < self.max_tokens:
            return CodeBlock(
                code=text,
                path=path,
                complete=True,
                start_line=node.start_point[0],
                end_line=node.end_point[0],
                depth=depth,
                id=node_id,
                parent_id=parent_id,
                children=[],
                language=self.language,
                type=node.type,
                tokens=block_length,
            )

        text_chunks = [child.text.decode() for child in node.children]
        lengths = list(map(self._count_tokens, text_chunks))
        longest_indices = sorted(range(len(lengths)), key=lengths.__getitem__)
        child_blocks = []

        # Replace child node code with placeholders until we can fit in context,
        #  starting with the longest children
        while self._count_tokens('\n'.join(text_chunks)) > self.max_tokens:
            longest_index = longest_indices.pop()
            child = self._recurse_split(
                node=node.children[longest_index],
                path=path,
                depth=depth+1,
                parent_id=node_id,
                id_gen=id_gen
            )
            text_chunks[longest_index] = f"{self.comment} {child.id}"
            child_blocks.append(child)

        return CodeBlock(
            code='\n'.join(text_chunks),
            path=path,
            complete=False,
            start_line=node.start_point[0],
            end_line=node.end_point[0],
            depth=depth,
            id=node_id,
            parent_id=parent_id,
            children=child_blocks,
            language=self.language,
            type=node.type,
            tokens=block_length,
        )

    def _count_tokens(self, code: str) -> int:
        """Count the number of tokens in the given code.

        Arguments:
            code: The code to count the number of tokens in.

        Returns:
            The number of tokens in the given code.
        """
        return self.model.get_num_tokens(code)

    def _git_clone(self, repository_url: str, destination_folder: Path | str) -> None:
        try:
            Repo.clone_from(repository_url, destination_folder)
            log.debug(f"{repository_url} cloned to {destination_folder}")
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    def _create_parser(
        self, so_file: Path | str, github_url: str, tree_sitter_lang_dir: str
    ) -> None:
        """Create the parser for the given language.

        Arguments:
            so_file: The path to the so file for the language.
        """
        tree_sitter_dir = Path.home() / ".tree-sitter"
        tree_sitter_dir.mkdir(exist_ok=True)
        lang_dir = tree_sitter_dir / tree_sitter_lang_dir

        if not lang_dir.exists():
            self._git_clone(github_url, lang_dir)

        tree_sitter.Language.build_library(
            # Store the library in the `build` directory
            str(so_file),
            [str(lang_dir)],
        )

    def _load_parser(self, build_dir: Path, github_url: str) -> None:
        """Load the parser for the given language.

        Sets `self.parser`'s language to the one specified in `self.language`.

        Arguments:
            build_dir: The directory to store the so file in.
            github_url: The url to the tree-sitter GitHub repository for the language.
        """
        so_filename = (
            f"{self.language}_parser_{platform.system()}_{platform.processor()}.so"
        )
        so_file = (build_dir / so_filename).__str__()
        try:
            self.parser.set_language(tree_sitter.Language(so_file, self.language))
        except OSError:
            log.warning(
                f"Could not load {so_file}, building one for {platform.system()} "
                f"system, with {platform.processor()} processor"
            )
            self._create_parser(so_file, github_url, f"tree-sitter-{self.language}")
            self._load_parser(build_dir, github_url)
