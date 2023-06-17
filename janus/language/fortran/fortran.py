from pathlib import Path
from typing import List

import numpy as np
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
                children=[],
                language=self.language,
                type="file",
                tokens=self._count_tokens(text),
            )
            out_block = block
        else:
            node = cursor.node
            out_block = self._recurse_split(node, path)
        self._blocks_to_file(out_block, "test.f90")
        return out_block

    def _recurse_split(self, node: tree_sitter.Node, path: Path) -> CodeBlock:
        """Recursively split the code into functional blocks.

        Arguments:
            cursor: A tree-sitter cursor to walk through the code.

        Returns:
            A CodeBlock object.
        """
        # First get the text for all the siblings at this level
        text = node.text.decode()
        # _, text = self._sibling_text(node, text)

        if self._count_tokens(text) < self.max_tokens:
            return CodeBlock(
                code=text,
                path=path,
                complete=True,
                parent_id=None,
                start_line=node.start_point[0],
                end_line=node.end_point[0],
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
                    new_text += f"<<<child_{child_idx}>>>\n"
                    child_idx += 1
                elif self._count_tokens(child_text) > self.max_tokens:
                    idxs.append(i)
                    new_text += f"<<<child_{child_idx}>>>\n"
                    child_idx += 1
                else:
                    new_text += f"{child_text}\n"

            if max_idx not in idxs:
                idxs.append(max_idx)

            children = []
            for i in idxs:
                children.append(self._recurse_split(node.children[i], path))

            return CodeBlock(
                code=new_text,
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

    def _sibling_text(self, node: tree_sitter.Node, text: str) -> str:
        """Get the text for all the siblings at this level.

        This is run recursively to get the text for all the siblings.

        Arguments:
            node: The tree-sitter node to get the siblings of.
            text: The text of the node.

        Returns:
            The node and the text of the siblings.
        """
        text = node.text.decode()
        if node.next_sibling is not None:
            node = node.next_sibling
            node, text = self._sibling_text(node, text)
            text += "\n" + text
        return node, text

    def _blocks_to_file(self, block: CodeBlock, path: Path) -> None:
        """Save the CodeBlock to a path.

        Arguments:
            block: The functional code block to save.
            path: The path to save the functional code block to.
        """
        with open(path, "w") as f:
            f.write(self._blocks_to_str(block.code, block))

    def _blocks_to_str(self, input: str, block: CodeBlock) -> None:
        """Convert a functional code block to a string.

        Arguments:
            block: The functional code block to convert to a string.
        """
        if len(block.children) == 0:
            return input
        else:
            for i, child in enumerate(block.children):
                if f"<<<child_{i}>>>" in child.code:
                    output = self._blocks_to_str(
                        input.replace(f"<<<child_{i}>>>", child.code), child
                    )
                else:
                    return input
            return output
