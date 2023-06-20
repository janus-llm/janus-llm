from ..utils.enums import LANGUAGE_COMMENTS, LANGUAGE_SUFFIXES
from .block import CodeBlock


class FileManager:
    """A parent class that manages the files that are being translated."""

    def __init__(self, language: str = "python") -> None:
        self.language: str = language
        self.comment: str = LANGUAGE_COMMENTS[self.language]
        self.suffix: str = LANGUAGE_SUFFIXES[self.language]

    def blocks_to_file(self, block: CodeBlock) -> None:
        """Save the CodeBlock to a path.

        Arguments:
            block: The functional code block to save.
        """
        code_str = self._blocks_to_str(block.code, block)
        block.path.write_text(code_str, encoding="utf-8")

    def _blocks_to_str(self, input: str, block: CodeBlock) -> str:
        """Recursively convert a functional code block to a string.

        # TODO: Fix the formatting issues with this method. It currently doesn't get
        the indentation or number of newlines correct. But I feel that it would have
        to be done differently to keep track of that sort of thing within the
        `CodeBlock` when originally splitting.

        Arguments:
            input: The input string to replace with the children of `block`.
            block: The functional code block to recursively replace children.

        Returns:
            The string with the children of `block` inserted. It should replace the
            whole tree of CodeBlocks to get the original code (with some formatting
            issues)
        """
        if len(block.children) == 0:
            return input
        else:
            for i, child in enumerate(block.children):
                if f"{self.comment} <<<child_{i}>>>" in block.code:
                    output = self._blocks_to_str(
                        input.replace(f"{self.comment} <<<child_{i}>>>", child.code),
                        child,
                    )
                else:
                    return input
            return output
