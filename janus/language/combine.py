from ..utils.logger import create_logger
from .block import CodeBlock, TranslatedCodeBlock
from .file import FileManager

log = create_logger(__name__)


class Combiner(FileManager):
    """Combine files that have been split into functional blocks back into a single
    file.
    """

    def __init__(self, language: str = "python") -> None:
        """Initialize a Combiner instance.

        Arguments:
            language: The name of the language to combine.
        """
        super().__init__(language)

    def combine(self, block: CodeBlock) -> None:
        self.combine_children(block)
        block.text = block.prefix + block.text + block.suffix

    def combine_children(self, block: CodeBlock) -> None:
        """Recursively combine block text with children text.

        TODO: Fix the formatting issues with this method. It currently doesn't get
        the indentation or number of newlines correct. But I feel that it would have
        to be done differently to keep track of that sort of thing within the
        `CodeBlock` when originally splitting.

        Update from Chris: The best way to go about this would be to track
        bytes between nodes with tree_sitter's byte indexing.

        Arguments:
            block: The functional text block to recursively replace children.
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
        if block.text is None:
            children = sorted(block.children, key=lambda b: b.start_byte)
            block.text = "".join(
                [
                    children[0].prefix,
                    *[c.text + c.suffix for c in children],
                ]
            )
            block.children = []
            block.complete = children_complete
            return

        # Replace all placeholders
        missing_children = []
        for child in block.children:
            if isinstance(block, TranslatedCodeBlock) and not child.translated:
                missing_children.append(child)
                continue
            if not self.contains_child(block.text, child):
                missing_children.append(child)
                continue
            block.text = block.text.replace(
                self._placeholder(child),
                child.prefix + child.text + child.suffix,
            )

        if missing_children:
            missing_ids = [c.id for c in missing_children]
            log.warning(f"Some children not found in text: {missing_ids}")

        block.children = missing_children
        block.complete = children_complete and not missing_children

    def contains_child(self, code: str, child: CodeBlock) -> bool:
        """Determine whether the given text contains a placeholder for the given
        child block.
        """
        return code is None or self._placeholder(child) in code

    def count_missing(self, input_block: CodeBlock, output_code: str) -> int:
        """Return the number of children of input_block who are not represented
        in output_code with a placeholder

        Arguments:
            input_block: The block to check for missing children
            output_code: The text to check for placeholders

        Returns:
            The number of children of input_block who are not represented in
            output_code with a placeholder
        """
        missing_children = 0
        for child in input_block.children:
            if not self.contains_child(output_code, child):
                missing_children += 1
        return missing_children

    def _placeholder(self, child: CodeBlock) -> str:
        """Get the placeholder to represent the text of the given block

        Arguments:
            child: The block to get the placeholder for

        Returns:
            The placeholder to represent the text of the given block
        """
        return f"<<<{child.id}>>>"
