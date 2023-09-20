import re
from itertools import count, groupby
from pathlib import Path
from typing import List, Tuple, Callable, Hashable

from langchain.schema.language_model import BaseLanguageModel

from ...utils.logger import create_logger
from ..block import CodeBlock
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

    def __init__(
        self,
        model: BaseLanguageModel,
        max_tokens: int = 4096,
        maximize_block_length: bool = False,
        force_split: bool = False,
    ) -> None:
        """Initialize a MumpsSplitter instance.

        Arguments:
            max_tokens: The maximum number of tokens supported by the model
            maximize_block_length: Whether to greedily merge blocks back together
                after splitting in order to maximize the context sent to the LLM
        """
        # MUMPS code tends to take about 2/3 the space of Python
        self.max_tokens: int = int(max_tokens * 2 / 5)
        self.model = model
        self.language: str = "mumps"
        self.comment: str = ";"
        super().__init__(max_tokens=max_tokens, model=model, language='mumps')

        self.maximize_block_length = maximize_block_length
        self.force_split = force_split

    @classmethod
    def _regex_split(cls, code: str):
        return re.split(cls.patterns[0].start, code)

    def _get_ast(self, code: str | bytes) -> ASTNode:
        code = str(code)

        split_code = self._regex_split(code)
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

            first_label = re.search(f"^(\w+)", chunk)
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

    def _get_id_function(self) -> Callable[[ASTNode], Hashable]:
        def id_gen(node: ASTNode) -> Hashable:
            """Generate a unique id for each child block.

            Returns:
                A unique id for each child block.
            """
            return f"<{node.name}>"
        return id_gen

    def _split(self, code: str | bytes, path: Path) -> CodeBlock:
        root = self._get_ast(code)
        return self._recurse_split(
            node=root,
            path=path,
            depth=0,
            parent_id=None,
            use_placeholders=False
        )
