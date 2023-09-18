from typing import List

from .file import FileManager
from ..utils.logger import create_logger
from .block import CodeBlock, TranslatedCodeBlock

log = create_logger(__name__)


class Combiner(FileManager):
    """No special functionality for the Combiner class yet."""

    def __init__(self, language: str = "python") -> None:
        """Initialize a Combiner instance.

        Arguments:
            language: The name of the language to combine.
        """
        super().__init__(language)

    def combine_children(self, block: CodeBlock) -> None:
        """Recursively combine block code with children code.

        TODO: Fix the formatting issues with this method. It currently doesn't get
         the indentation or number of newlines correct. But I feel that it would have
         to be done differently to keep track of that sort of thing within the
         `CodeBlock` when originally splitting.

        Arguments:
            block: The functional code block to recursively replace children.
        """
        if block.complete:
            return

        if isinstance(block, TranslatedCodeBlock) and not block.translated:
            return

        children_complete = True
        for child in block.children:
            self.combine_children(child)
            if not child.complete:
                children_complete = False

        # If input string is None, then this node consists exclusively of
        #  children with no other formatting. Simply concatenate the children.
        if block.code is None:
            children = sorted(block.children, key=lambda b: b.start_line)
            block.code = '\n'.join(child.code for child in children)
            block.complete = children_complete
            return

        missing_children = set()
        if isinstance(block, TranslatedCodeBlock):
            original_children = {child.id for child in block.original.children}
            translated_children = {child.id for child in block.children if child.translated}
            missing_children = original_children.difference(translated_children)

        # Replace all placeholders
        for child in block.children:
            if isinstance(block, TranslatedCodeBlock) and not child.translated:
                continue
            if not self.contains_child(block.code, child):
                missing_children.add(child.id)
                continue
            block.code = block.code.replace(self._placeholder(child), child.code)

        if missing_children:
            log.warning(f"Some children not found in code: {missing_children}")

        block.complete = children_complete and not missing_children

    def validate(self, code: str, input_block: CodeBlock) -> bool:
        missing_children = []
        for child in input_block.children:
            if not self.contains_child(code, child):
                missing_children.append(child.id)
        if missing_children:
            log.warning(f"Child placeholders not present in code: {missing_children}")
            log.debug(f"Code:\n{code}")
            return False
        return True

    def contains_child(self, code: str, child: CodeBlock) -> bool:
        return code is None or self._placeholder(child) in code

    def count_missing(self, input_block: CodeBlock, output_code: str) -> int:
        missing_children = 0
        for child in input_block.children:
            if not self.contains_child(output_code, child):
                missing_children += 1
        return missing_children

    def _placeholder(self, child) -> str:
        return f"{self.comment} {child.id}"
