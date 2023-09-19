import re
from itertools import count, groupby
from pathlib import Path
from typing import List, Tuple

from langchain.schema.language_model import BaseLanguageModel

from ...utils.logger import create_logger
from ..block import CodeBlock
from ..combine import Combiner
from ..splitter import Splitter
from .patterns import MumpsLabeledBlockPattern

log = create_logger(__name__)


class CumulativeLengthGrouper:
    """A helper class for merging code up to a maximum token length.
    Expected usage:
        grouper = CumulativeLengthGrouper(2048, tiktoken.encoding_for_model(model))
        groups = itertools.groupby(blocks, key=grouper)
        blocks = ['\n'.join(g) for _, g in groups]
    """

    tokenizer = None

    def __init__(self, max_tokens, model):
        self.max_tokens = max_tokens
        self.model: BaseLanguageModel = model

        self.group_ctr = count()
        self.cur_grp = next(self.group_ctr)
        self.cum_len = 0

    def __call__(self, block):
        block_length = self.model.get_num_tokens(block)
        self.cum_len += block_length
        # If accumulated length exceeds block limit...
        if self.cum_len > self.max_tokens:
            # Move to new group
            self.cur_grp = next(self.group_ctr)
            self.cum_len = block_length
        return self.cur_grp


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

    def _split(self, code: str, path: Path) -> CodeBlock:
        """Split the given file into functional code blocks.

        Arguments:
            code: A string containing the code of the entire file to split
            path: The path to the code

        Returns:
            A File dataclass containing the path to the file and all of its code blocks
        """
        block_length = self._count_tokens(code)

        # The whole file is one block
        if block_length < self.max_tokens and not self.force_split:
            return CodeBlock(
                code=code,
                path=path,
                complete=True,
                start_line=0,
                end_line=len(code.splitlines()),
                depth=0,
                id=0,
                parent_id=None,
                children=[],
                language=self.language,
                type="file",
                tokens=block_length,
            )

        split_code = self._regex_split(code)
        split_code = [t for s in split_code if (t := s.strip())]
        if self.maximize_block_length and not self.force_split:
            # Merge adjacent blocks back together to meet self.max_tokens
            grouper = CumulativeLengthGrouper(self.max_tokens, self.model)
            split_code = ["\n".join(grp) for _, grp in groupby(split_code, key=grouper)]

        seen_ids = set()

        def id_gen():
            block_id = f"<<<child_{len(seen_ids)}>>>"
            seen_ids.add(block_id)
            return block_id

        blocks: List[CodeBlock] = []
        start_line = 0
        for i, block in enumerate(split_code):
            block_id = id_gen()
            end_line = start_line + len(block.splitlines())

            # The entire block is under the token length
            if self._count_tokens(block) <= self.max_tokens:
                code_block = CodeBlock(
                    code=block,
                    path=path,
                    complete=True,
                    start_line=start_line,
                    end_line=end_line,
                    depth=1,
                    id=block_id,
                    parent_id="root",
                    children=[],
                    language=self.language,
                    type="file",
                    tokens=self._count_tokens(block),
                )
            # The whole block is too long, split into segments
            else:
                segments = self._recurse_divide(block)
                subblocks = []
                seg_start_line = start_line
                for j, segment in enumerate(segments):
                    seg_end_line = seg_start_line + len(segment.splitlines())
                    code_block = CodeBlock(
                        code=segment,
                        path=path,
                        complete=True,
                        start_line=seg_start_line,
                        end_line=seg_end_line,
                        depth=2,
                        id=id_gen(),
                        parent_id=block_id,
                        children=[],
                        language=self.language,
                        type="",
                        tokens=self._count_tokens(segment),
                    )
                    seg_start_line = seg_end_line
                    subblocks.append(code_block)
                code_block = CodeBlock(
                    code=None,
                    path=path,
                    complete=False,
                    start_line=start_line,
                    end_line=end_line,
                    depth=1,
                    id=block_id,
                    parent_id="root",
                    children=subblocks,
                    language=self.language,
                    type="file",
                    tokens=0,
                )
            start_line = end_line
            blocks.append(code_block)

        return CodeBlock(
            code=None,
            path=path,
            complete=False,
            start_line=0,
            end_line=len(code.splitlines()),
            depth=0,
            id="root",
            parent_id=None,
            children=blocks,
            language=self.language,
            type="file",
            tokens=0,
        )

    def _recurse_divide(self, code: str) -> List[str]:
        """Recursively splt the code in half (by line) until each segment is
        smaller than the token limit.

        Arguments:
            code: The block to split into segments.

        Returns:
            A list of segments.
        """
        if self._count_tokens(code) <= self.max_tokens:
            return [code]
        else:
            lines = code.splitlines()
            split_idx = len(lines) // 2
            left = "\n".join(lines[:split_idx])
            right = "\n".join(lines[split_idx:])
            return self._recurse_divide(left) + self._recurse_divide(right)
