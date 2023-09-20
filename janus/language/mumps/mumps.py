import re
from typing import Tuple, Callable, Hashable
from collections import defaultdict

from langchain.schema.language_model import BaseLanguageModel

from ...utils.logger import create_logger
from ..combine import Combiner
from ..splitter import Splitter
from .patterns import MumpsLabeledBlockPattern
from ..node import ASTNode, NodeType

log = create_logger(__name__)


class MumpsCombiner(Combiner):
    """A class that combines code blocks into mumps files."""

    def __init__(self) -> None:
        """Initialize a MumpsCombiner instance."""
        super().__init__("mumps")


class MumpsSplitter(Splitter):
    """A class for splitting MUMPS code into functional blocks to prompt with for
    transcoding.

    Attributes:
        patterns: A tuple of `Pattern`s to use for splitting Mumps code into
            functional blocks.
    """

    patterns: Tuple[MumpsLabeledBlockPattern, ...] = (MumpsLabeledBlockPattern(),)

    def __init__(self, model: BaseLanguageModel, max_tokens: int = 4096):
        """Initialize a MumpsSplitter instance.

        Arguments:
            max_tokens: The maximum number of tokens supported by the model
        """
        super().__init__(
            language='mumps',
            model=model,
            max_tokens=max_tokens,
            use_placeholders=False,
        )

        # MUMPS code tends to take about 2/3 the space of Python
        self.max_tokens: int = int(max_tokens * 2 / 5)

    def _reset_id_function(self) -> None:
        self.seen_ids = defaultdict(list)

    def _get_id_function(self) -> Callable[[ASTNode], Hashable]:
        def id_gen(node: ASTNode) -> Hashable:
            """Generate a unique id for each child block.

            Returns:
                A unique id for each child block.
            """
            return f"<{node.name}>"
        return id_gen

    def _generate_id(self, node, *args, **kwargs) -> Hashable:
        block_id = f"<{node.name}-{len(self.seen_ids[node.name])+1}>"
        self.seen_ids[node.name].append(block_id)
        return block_id

    def _get_ast(self, code: str | bytes) -> ASTNode:
        code = str(code)

        split_code = re.split(self.patterns[0].start, code)
        prefixes = ['']+split_code[1::2]
        chunks = split_code[::2]
        suffixes = split_code[1::2]
        start_line = 0
        start_byte = 0
        nodes = []
        for prefix, chunk, suffix in zip(prefixes, chunks, suffixes):
            start_byte += len(bytes(prefix, "utf-8"))
            start_line += prefix.count('\n')
            end_byte = start_byte + len(bytes(chunk, "utf-8"))
            end_line = start_line + chunk.count('\n')
            end_char = len(chunk.rsplit('\n', 1)[-1])

            first_label = re.search(r"^(\w+)", chunk)
            name = first_label.groups(1)[0] if first_label is not None else 'anon'

            nodes.append(ASTNode(
                text=chunk,
                name=name,
                start_point=(start_line, 0),
                end_point=(end_line, end_char),
                start_byte=start_byte,
                end_byte=end_byte,
                prefix=prefix,
                suffix=suffix,
                type=NodeType('subroutine'),
                children=[]
            ))
            start_byte = end_byte
            start_line = end_line
        return ASTNode(
                text=code,
                name="root",
                start_point=(0, 0),
                end_point=(len(code.split('\n')), 0),
                start_byte=0,
                end_byte=len(bytes(code, "utf-8")),
                prefix='',
                suffix='',
                type=NodeType('routine'),
                children=nodes
        )
