import platform
from pathlib import Path

import numpy as np
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
        if self._count_tokens(text := cursor.node.text.decode()) < self.max_tokens:
            block = CodeBlock(
                code=text,
                path=path,
                complete=True,
                start_line=0,
                end_line=len(text.splitlines()),
                depth=0,
                id=0,
                children=[],
                language=self.language,
                type="file",
                tokens=self._count_tokens(text),
            )
            out_block = block
        else:
            node = cursor.node
            out_block = self._recurse_split(node, path, 0, 0)
        return out_block

    def _recurse_split(
        self, node: tree_sitter.Node, path: Path, depth: int, id: int
    ) -> CodeBlock:
        """Recursively split the code into functional blocks.

        Arguments:
            node: The current node in the tree.
            path: The path to the file containing the code.
            depth: The current depth of the recursion.
            id: The current id of the child block at depth `N`.

        Returns:
            A CodeBlock object.
        """
        # First get the text for all the siblings at this level
        text = node.text.decode()

        # If the text at the function input is less than the max tokens, then we can
        # just return it as a CodeBlock with no children.
        if self._count_tokens(text) < self.max_tokens:
            return CodeBlock(
                code=text,
                path=path,
                complete=True,
                start_line=node.start_point[0],
                end_line=node.end_point[0],
                depth=depth,
                id=id,
                children=[],
                language=self.language,
                type=node.type,
                tokens=self._count_tokens(text),
            )
        # Otherwise, we need to split the text into smaller blocks.
        else:
            # First, we need to find the child with the most tokens.
            idxs = []
            child_idx = 0
            new_text = ""
            max_idx = np.argmax(
                [self._count_tokens(c.text.decode()) for c in node.children]
            )
            # Then, we need to find all of the child blocks that exceed the max tokens.
            for i, child in enumerate(node.children):
                child_text = child.text.decode()
                # If the child is the one with the most tokens, then we need to split it
                if i == max_idx:
                    idxs.append(i)
                    new_text += f"{self.comment} <<<child_{child_idx}>>>\n"
                    child_idx += 1
                # If the child is not the one with the most tokens, but it exceeds the
                # max tokens, then we need to split it
                elif self._count_tokens(child_text) > self.max_tokens:
                    idxs.append(i)
                    new_text += f"{self.comment} <<<child_{child_idx}>>>\n"
                    child_idx += 1
                # Otherwise, we can just add the child text to the new text
                else:
                    new_text += f"{child_text}\n"

            if max_idx not in idxs:
                idxs.append(max_idx)

            # If we get through all the children, but `new_text` still exceeds the token
            # limit, then we need replace more children at this level.
            while self._count_tokens(new_text) > self.max_tokens:
                # Get the indices of the children that we haven't already added to the
                # new text
                temp_idxs = [i for i in range(len(node.children)) if i not in idxs]
                # Get the child with the most tokens
                max_child_idx = np.argmax(
                    [
                        self._count_tokens(node.children[i].text.decode())
                        for i in temp_idxs
                    ]
                )
                replaced_child_idx = temp_idxs[max_child_idx]
                max_text = node.children[replaced_child_idx].text.decode()
                # Replace the child with the most tokens with a placeholder
                new_text = new_text.replace(
                    max_text, f"{self.comment} <<<child_{child_idx}>>>\n"
                )
                idxs.append(replaced_child_idx)
                child_idx += 1

            children = []
            for child_idx, i in enumerate(idxs):
                children.append(
                    self._recurse_split(node.children[i], path, depth + 1, child_idx)
                )

            return CodeBlock(
                code=new_text,
                path=path,
                complete=False,
                start_line=node.start_point[0],
                end_line=node.end_point[0],
                depth=depth,
                id=id,
                children=children,
                language=self.language,
                type=node.type,
                tokens=self._count_tokens(new_text),
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
