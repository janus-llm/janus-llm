from ..utils.logger import create_logger
from .block import CodeBlock, TranslatedCodeBlock
from .file import FileManager

log = create_logger(__name__)


class Combiner(FileManager):
    """Combine files that have been split into functional blocks back into
    a single file.
    """

    @staticmethod
    def combine(block: CodeBlock) -> None:
        Combiner.combine_children(block)
        block.omit_prefix = False

    @staticmethod
    def combine_children(block: CodeBlock) -> None:
        """Recursively combine block code with children code.

        Arguments:
            block: The functional code block to recursively replace children.
        """
        if block.complete:
            return

        if isinstance(block, TranslatedCodeBlock) and not block.translated:
            return

        children_complete = True
        for child in block.children:
            Combiner.combine_children(child)
            if not child.complete:
                children_complete = False

        # If input string is None, then this node consists exclusively of
        #  children with no other formatting. Simply concatenate the children.
        if block.text is None:
            children = sorted(block.children)
            block.text = "".join([c.complete_text for c in children])
            block.children = []
            block.complete = children_complete
            return

        # Replace all placeholders
        missing_children = []
        for child in block.children:
            if isinstance(block, TranslatedCodeBlock) and not child.translated:
                missing_children.append(child)
                continue
            if not Combiner.contains_child(block.text, child):
                missing_children.append(child)
                continue
            block.text = block.text.replace(child.placeholder, child.text)

        if missing_children:
            missing_ids = [c.id for c in missing_children]
            log.warning(f"Some children not found in code: {missing_ids}")

        block.children = missing_children
        block.complete = children_complete and not missing_children

    @staticmethod
    def contains_child(code: str, child: CodeBlock) -> bool:
        """Determine whether the given code contains a placeholder for the given
        child block.
        """
        return code is None or child.placeholder in code

    @staticmethod
    def count_missing(input_block: CodeBlock, output_code: str) -> int:
        """Return the number of children of input_block who are not represented
        in output_code with a placeholder

        Arguments:
            input_block: The block to check for missing children
            output_code: The code to check for placeholders

        Returns:
            The number of children of input_block who are not represented in
            output_code with a placeholder
        """
        missing_children = 0
        for child in input_block.children:
            if not Combiner.contains_child(output_code, child):
                missing_children += 1
        return missing_children
