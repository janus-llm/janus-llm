from janus.language.block import CodeBlock, TranslatedCodeBlock
from janus.language.file import FileManager
from janus.utils.logger import create_logger

log = create_logger(__name__)


class Combiner(FileManager):
    """Combine files that have been split into functional blocks back into
    a single file.
    """

    @staticmethod
    def combine(root: CodeBlock) -> None:
        """Combine the given block with its children.

        Arguments:
            root: The functional code block to combine with its children.
        """
        Combiner.combine_children(root)
        root.omit_prefix = False

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
            block.complete = children_complete
            return

        missing_children = []
        for child in block.children:
            if isinstance(block, TranslatedCodeBlock) and not child.translated:
                missing_children.append(child)
                continue

        if missing_children:
            missing_ids = [c.id for c in missing_children]
            log.warning(f"Some children not found in code: {missing_ids}")

        block.children = missing_children
        block.complete = children_complete and not missing_children


class JsonCombiner(Combiner):
    @staticmethod
    def combine(root: CodeBlock) -> None:
        """Combine the given block with its children.

        Arguments:
            root: The functional code block to combine with its children.
        """
        stack = [root]
        while stack:
            block = stack.pop()
            if block.children:
                stack.extend(block.children)
                block.affixes = ("", "")
            else:
                block.affixes = ("\n", "\n")
        super(JsonCombiner, JsonCombiner).combine(root)


class ChunkCombiner(Combiner):
    @staticmethod
    def combine(root: CodeBlock) -> None:
        """A combiner which doesn't actually combine the code blocks,
        instead preserving children

        Arguments:
            root: The functional code block to combine with its children.
        """
        return root
