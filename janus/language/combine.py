from typing import List

from .file import FileManager
from ..utils.logger import create_logger
from .block import CodeBlock

log = create_logger(__name__)


class Combiner(FileManager):
    """No special functionality for the Combiner class yet."""

    def __init__(self, language: str = "python") -> None:
        """Initialize a Combiner instance.

        Arguments:
            language: The name of the language to combine.
        """
        super().__init__(language)

    def blocks_to_file(self, block: CodeBlock) -> None:
        """Save the CodeBlock to a path.

        Arguments:
            block: The functional code block to save.
        """
        code_str = self._blocks_to_str(block)
        block.path.write_text(code_str, encoding="utf-8")

    def _blocks_to_str(self, block: CodeBlock) -> str:
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
            return str(block.code)

        # If input string is None, then this node consists exclusively of
        #  children with no other formatting. Simply concatenate the children.
        if block.code is None:
            children = sorted(block.children, key=lambda b: b.start_line)
            output = [self._blocks_to_str(child) for child in children]
            return '\n'.join(output)

        output = block.code
        for child in block.children:
            placeholder = f"{self.comment} {child.id}"
            if placeholder not in block.code:
                log.warning("Not all children found in output!")
            output = output.replace(placeholder, self._blocks_to_str(child))

        return output

    def validate(self, code: str, input_block: CodeBlock) -> bool:
        missing = self._find_missing_placeholders(code, input_block)
        if missing:
            log.warning(f"Child placeholders not present in code: {missing}")
            log.debug(f"Code:\n{code}")
            return False
        return True

    def _find_missing_placeholders(self, code, input_block) -> List[str]:
        missing_placeholders = []
        for child in input_block.children:
            if f"{self.comment} {child.id}" not in code:
                missing_placeholders.append(child.id)
        return missing_placeholders
