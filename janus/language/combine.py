import re

from janus.language.block import CodeBlock
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
        root.mark_first()
        root.mark_last()

    @staticmethod
    def combine_children(block: CodeBlock) -> None:
        """Recursively combine block code with children code.

        Arguments:
            block: The functional code block to recursively replace children.
        """
        block.rebuild_text_from_children()
        block.complete = True


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


class PartitionCombiner(Combiner):
    @staticmethod
    def combine(root: CodeBlock) -> None:
        """A combiner which inserts partition tags between code blocks"""
        queue = [root]
        while queue:
            block = queue.pop(0)
            if block.children:
                queue.extend(block.children)
            else:
                block.affixes = (block.prefix, block.suffix + "\n<JANUS_PARTITION>\n")

        super(PartitionCombiner, PartitionCombiner).combine(root)
        root.text = re.sub(r"(?:\n<JANUS_PARTITION>\n)+$", "", root.text)
        root.affixes = (
            root.prefix,
            re.sub(r"(?:\n<JANUS_PARTITION>\n)+$", "", root.suffix),
        )
