from pathlib import Path
from typing import List

import tree_sitter

from ...utils.logger import create_logger
from ..block import CodeBlock
from ..splitter import Splitter

TREE_SITTER_FORTRAN_SO: Path = Path("janus/language/fortran/build_files/parser.so")

log = create_logger(__name__)


class FortranSplitter(Splitter):
    """A class for splitting Fortran code into functional blocks to prompt for
       transcoding.

    Attributes:
        patterns: A tuple of `Pattern`s to use for splitting Fortran code into
                  functional blocks.
        max_tokens: The maximum number of tokens to use for each functional block.
    """

    def __init__(
        self,
        patterns: List[str],
        max_tokens: int = 4096,
    ) -> None:
        """Initialize a Fortran instance.

        Arguments:
            patterns: A tuple of `Pattern`s to use for splitting Fortran code into
                      functional blocks.
        """
        super().__init__(patterns, max_tokens)
        self.language: str = "fortran"
        self.parser: tree_sitter.Parser = tree_sitter.Parser()
        try:
            self.parser.set_language(
                tree_sitter.Language(TREE_SITTER_FORTRAN_SO, self.language)
            )
        except OSError:
            log.warning(f"Could not load {TREE_SITTER_FORTRAN_SO}, trying mac version.")
            self.parser.set_language(
                tree_sitter.Language(
                    TREE_SITTER_FORTRAN_SO.parent
                    / f"{TREE_SITTER_FORTRAN_SO.stem}_mac.so",
                    self.language,
                )
            )

    def _split(self, code: str | bytes, path: Path) -> List[CodeBlock]:
        """Use tree-sitter to walk through the code and split into functional code blocks.

        The functional code blocks will have children if each individual code block
        doesn't fit within `self.max_tokens`.

        Arguments:
            code: The code to split up.
            path: The path to the file containing the code.

        Returns:
            A list of functional code blocks.
        """
        out_blocks = []
        if isinstance(code, str):
            code = bytes(code, "utf-8")

        tree = self.parser.parse(code)
        cursor = tree.walk()
        if self._count_tokens(text := cursor.node.text.decode()) < self.max_tokens:
            block = CodeBlock(
                code=text,
                path=path,
                complete=True,
                parent_id=None,
                start_line=0,
                end_line=len(text.splitlines()),
                children=None,
                language=self.language,
                type="file",
                tokens=self._count_tokens(text),
            )
            out_blocks.append(block)
        else:
            node = cursor.node
            out_blocks.append(self._recurse_split(node, path))
        return out_blocks

    def _recurse_split(self, node: tree_sitter.Node, path: Path) -> CodeBlock:
        """Recursively split the code into functional blocks.

        Arguments:
            cursor: A tree-sitter cursor to walk through the code.

        Returns:
            A CodeBlock object.
        """
        text = node.text.decode()
        if self._count_tokens(text) < self.max_tokens:
            return CodeBlock(
                code=text,
                path=path,
                complete=True,
                parent_id=None,
                start_line=node.start_point[0],
                end_line=node.end_point[0],
                children=None,
                language=self.language,
                type=node.type,
                tokens=self._count_tokens(text),
            )
        else:
            children = []
            # if node.next_sibling:
            #     new_text = text + node.next_sibling.text.decode()
            #     if self._count_tokens(new_text) < self.max_tokens:
            #         text = new_text
            #         node = node.next_sibling
            for child in node.children:
                children.append(self._recurse_split(child, path))
            return CodeBlock(
                code=text,
                path=path,
                complete=False,
                parent_id=None,
                start_line=node.start_point[0],
                end_line=node.end_point[0],
                children=children,
                language=self.language,
                type=node.type,
                tokens=self._count_tokens(text),
            )
