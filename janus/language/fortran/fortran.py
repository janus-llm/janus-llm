import tree_sitter

from ...utils.logger import create_logger
from ..splitter import Splitter

TREE_SITTER_FORTRAN_SO: str = "janus/language/fortran/parser.so"

log = create_logger(__name__)


class FortranSplitter(Splitter):
    """A class for splitting Fortran code into functional blocks to prompt for
       transcoding.

    Attributes:
        patterns: A tuple of `Pattern`s to use for splitting Fortran code into
                  functional blocks.
    """

    def __init__(
        self,
        patterns: list[str],
        max_tokens: int = 4096,
    ) -> None:
        """Initialize a Fortran instance.

        Arguments:
            patterns: A tuple of `Pattern`s to use for splitting Fortran code into
                      functional blocks.
        """
        super().__init__(patterns, max_tokens)
        self.language: str = "fortran"
        self.parser = tree_sitter.Parser()
        self.parser.set_language(
            tree_sitter.Language(TREE_SITTER_FORTRAN_SO, self.language)
        )

    def __call__(self, code: str | bytes) -> list[str]:
        """Split the input raw code string into a list of functional blocks.

        Arguments:
            code: A raw code string to split into functional blocks.

        Returns:
            A list of functional blocks
        """
        out_blocks = []
        if isinstance(code, str):
            code = bytes(code, "utf-8")
        tree = self.parser.parse(code)
        cursor = tree.walk()
        if self._count_tokens(text := cursor.node.text.decode()) < self.max_tokens:
            return [text]
        cursor.goto_first_child()
        text = ""
        cur_tokens = 0
        while cursor.node.type != "translation_unit":
            if (
                cur_tokens
                + (
                    new_tokens := self._count_tokens(
                        new_text := cursor.node.text.decode()
                    )
                )
                < self.max_tokens
            ):
                text += "\n" + new_text
                cur_tokens += new_tokens
                if not cursor.goto_next_sibling():
                    cursor.goto_parent()
                continue
            else:
                if text != "":
                    out_blocks.append(text)
                    text = ""
                    cur_tokens = 0
                    continue
                else:
                    if not cursor.goto_first_child():
                        raise RuntimeError(
                            "Current block is too large to meet token limit and has no"
                            " children to walk to"
                        )

        return out_blocks
