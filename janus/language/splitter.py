from pathlib import Path

import numpy as np
import tiktoken
import tree_sitter

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

    def __init__(
        self,
        max_tokens: int = 4096,
        model: str = "gpt-3.5-turbo",
        maximize_block_length: bool = False,
    ) -> None:
        """Initialize a Splitter instance.

        Arguments:
            max_tokens: The maximum number of tokens to use for each functional block.
            model: The name of the model to use for translation.
        """
        # Make sure `self.language` is set before calling `super().__init__` in
        # subclasses of `Splitter`
        super().__init__(language=self.language)
        # Divide max_tokens by 2 because we want to leave just as much space for the
        # prompt as for the translated code.
        self.max_tokens: int = max_tokens // 3
        self.maximize_block_length = maximize_block_length

        self.parser: tree_sitter.Parser = tree_sitter.Parser()

        # Using tiktoken as the tokenizer because that's what's recommended for OpenAI
        # models.
        self._tokenizer = tiktoken.encoding_for_model(model)

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
        else:
            idxs = []
            child_idx = 0
            new_text = ""
            max_idx = np.argmax(
                [self._count_tokens(c.text.decode()) for c in node.children]
            )
            for i, child in enumerate(node.children):
                child_text = child.text.decode()
                if i == max_idx:
                    idxs.append(i)
                    new_text += f"{self.comment} <<<child_{child_idx}>>>\n"
                    child_idx += 1
                elif self._count_tokens(child_text) > self.max_tokens:
                    idxs.append(i)
                    new_text += f"{self.comment} <<<child_{child_idx}>>>\n"
                    child_idx += 1
                else:
                    new_text += f"{child_text}\n"

            if max_idx not in idxs:
                idxs.append(max_idx)

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
                tokens=self._count_tokens(text),
            )

    def _count_tokens(self, code: str) -> int:
        """Count the number of tokens in the given code.

        Arguments:
            code: The code to count the number of tokens in.

        Returns:
            The number of tokens in the given code.
        """
        tokens = self._tokenizer.encode(code)
        return len(tokens)

    def _load_parser(self, so_file: Path | str) -> None:
        """Load the parser for the given language.

        Sets `self.parser`'s language to the one specified in `self.language`.

        Arguments:
            so_file: The path to the so file for the language.
        """
        try:
            self.parser.set_language(tree_sitter.Language(so_file, self.language))
        except OSError:
            log.warning(f"Could not load {so_file}, trying mac version.")
            try:
                self.parser.set_language(
                    tree_sitter.Language(
                        so_file.parent / f"{so_file.stem}_mac.so",
                        self.language,
                    )
                )
            except OSError:
                log.error(f"Could not load {so_file} or {so_file.stem}_mac.so")
