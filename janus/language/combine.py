from typing import Optional

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
        code_str = self._blocks_to_str(block.code, block)
        block.path.write_text(code_str, encoding="utf-8")

    def _blocks_to_str(self, code: Optional[str], block: CodeBlock) -> str:
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
            return str(code)

        # If input string is None, then this node consists exclusively of
        #  children with no other formatting. Simply concatenate the children.
        if code is None:
            children = sorted(block.children, key=lambda b: b.start_line)
            output = [self._blocks_to_str(child.code, child) for child in children]
            return '\n'.join(output)

        output = code
        for child in block.children:
            placeholder = f"{self.comment} {child.id}"
            if placeholder not in block.code:
                log.warning("Not all children found in output!")
                return code

            output = output.replace(placeholder, child.code)
            output = self._blocks_to_str(output, child)

        return output

    def validate(self, code: str, input_block: CodeBlock) -> bool:
        for child in input_block.children:
            placeholder = f"{self.comment} {child.id}"
            if placeholder not in code:
                log.warning(f"Child placeholder ({child.id}) not present in code")
                log.debug(f"Code:\n{code}")
                return False
        return True
