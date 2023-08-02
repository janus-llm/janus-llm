import re
from itertools import count, groupby
from pathlib import Path
from typing import List, Tuple

import tiktoken

from ...utils.logger import create_logger
from ..block import CodeBlock
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

    def __init__(self, max_tokens, tokenizer):
        self.max_tokens = max_tokens
        self.tokenizer = tokenizer

        self.group_ctr = count()
        self.cur_grp = next(self.group_ctr)
        self.cum_len = 0

    def __call__(self, block):
        block_length = len(self.tokenizer.encode(block))
        self.cum_len += block_length
        # If accumulated length exceeds block limit...
        if self.cum_len > self.max_tokens:
            # Move to new group
            self.cur_grp = next(self.group_ctr)
            self.cum_len = block_length
        return self.cur_grp


class MumpsSplitter(Splitter):
    """A class for splitting MUMPS code into functional blocks to prompt with for
    transcoding.

    Attributes:
        patterns: A tuple of `Pattern`s to use for splitting Mumps code into
            functional blocks.
    """
    patterns: Tuple[MumpsLabeledBlockPattern, ...] = (MumpsLabeledBlockPattern(),)

    def __init__(self, max_tokens: int = 4096, model: str = "gpt-3.5-turbo",
                 maximize_block_length: bool = False) -> None:
        """Initialize a MumpsSplitter instance.

        Arguments:
            patterns: A tuple of `Pattern`s to use for splitting MUMPS code into
                functional blocks.
        """
        self.language: str = "mumps"
        self.comment: str = ";"
        super().__init__(max_tokens=max_tokens, model=model)

        # MUMPS code tends to take about 2/3 the space of Python
        self.max_tokens: int = int(max_tokens * 2/5)
        self.maximize_block_length = maximize_block_length

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

        # The whole file is one block
        if self._count_tokens(code) < self.max_tokens:
            return CodeBlock(
                code=code,
                path=path,
                complete=True,
                start_line=0,
                end_line=len(code.splitlines()),
                depth=0,
                id=0,
                children=[],
                language=self.language,
                type="file",
                tokens=self._count_tokens(code),
            )

        blocks = self._regex_split(code)
        if self.maximize_block_length:
            # Merge adjacent blocks back together to meet self.max_tokens
            grouper = CumulativeLengthGrouper(self.max_tokens, self._tokenizer)
            blocks = ["\n".join(grp) for _, grp in groupby(blocks, key=grouper)]

        components: List[CodeBlock] = []
        start_line = 0
        for block in blocks:
            # The entire block is under the token length
            if self._count_tokens(block) <= self.max_tokens:
                end_line = start_line + len(block.splitlines())
                code_block = CodeBlock(
                    code=block,
                    path=path,
                    complete=True,
                    start_line=start_line,
                    end_line=end_line,
                    depth=0,
                    id=0,
                    children=[],
                    language=self.language,
                    type="file",
                    tokens=self._count_tokens(block),
                )
                start_line = end_line
                components.append(code_block)
            # The whole block is too long, split into segments
            else:
                segments = self._split_block_into_segs(block)
                for segment_id, segment in enumerate(segments):
                    end_line = start_line + len(segment.splitlines())
                    code_block = CodeBlock(
                        code=segment,
                        path=path,
                        complete=True,
                        start_line=start_line,
                        end_line=end_line,
                        depth=1,
                        id=segment_id,
                        children=[],
                        language=self.language,
                        type="",
                        tokens=self._count_tokens(segment),
                    )
                    start_line = end_line
                    components.append(code_block)
        main_block = ""
        for i in range(len(components)):
            main_block += f"{self.comment} <<<child_{i}>>>\n"
        return CodeBlock(
            code=main_block,
            path=path,
            complete=False,
            start_line=0,
            end_line=len(code.splitlines()),
            depth=0,
            id=0,
            children=components,
            language=self.language,
            type="file",
            tokens=self._count_tokens(code),
        )

    def _split_block_into_segs(self, block: str) -> Tuple[str]:
        """Recursively splt the block string in half until each segment is smaller than
        the token limit.

        Arguments:
            block: The block to split into segments.

        Returns:
            A tuple of segments.
        """
        if self._count_tokens(block) <= self.max_tokens:
            return (block,)
        else:
            split_idx = len(block) // 2
            return self._split_block_into_segs(
                block[:split_idx]
            ) + self._split_block_into_segs(block[split_idx:])
