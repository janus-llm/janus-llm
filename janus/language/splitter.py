import re
from pathlib import Path
from typing import List, Optional, Tuple
from itertools import count, groupby

import tiktoken

from ..utils.logger import create_logger
from .block import CodeBlock, File
from .pattern import Pattern

log = create_logger(__name__)


class CumulativeLengthGrouper:
    """A helper class for merging code up to a maximum token length.
    Expected usage:
        grouper = CumulativeLengthGrouper(2048, tiktoken.encoding_for_model("gpt-3.5-turbo"))
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


class Splitter:
    """A class for splitting code into functional blocks to prompt with for
    transcoding.
    """

    def __init__(
        self,
        patterns: Tuple[Pattern, ...],
        max_tokens: int = 4096,
        model: str = "gpt-3.5-turbo",
        maximize_block_length: bool = False
    ) -> None:
        """Initialize a Splitter instance.

        Arguments:
            patterns: A tuple of `Pattern`s to use for splitting code into
                functional blocks.
            max_tokens: The maximum number of tokens that the given model can
                hold in context
        """

        self.patterns: Tuple[Pattern, ...] = patterns
        # Divide max_tokens by 2 because we want to leave just as much space for the
        # prompt as for the translated code.
        self.max_tokens: int = max_tokens // 3
        self.language: Optional[str] = None
        self.comment: Optional[str] = None

        self.maximize_block_length = maximize_block_length

        # Using tiktoken as the tokenizer because that's what's recommended for OpenAI
        # models.
        self._tokenizer = tiktoken.encoding_for_model(model)

    def split(self, file: Path | str) -> File:
        """Split the given file into functional code blocks.

        Arguments:
            file: The file to split into functional blocks.

        Returns:
            A tuple of functional blocks.
        """
        path = Path(file)
        code = path.read_text()
        return self._split(code, path)

    def _split(self, code: str, path: Path) -> File:
        """Split the given file into functional code blocks.

        Arguments:
            code: A string containing the code of the entire file to split
            path: The path to the code

        Returns:
            A File dataclass containing the path to the file and all of its code blocks
        """
        components: List[CodeBlock] = []

        total_tokens = self._count_tokens(code)

        # The whole file is one block
        if total_tokens <= self.max_tokens:
            block = CodeBlock(
                code=code,
                path=path,
                complete=True,
                block_id=0,
                segment_id=0,
                language=self.language,
                type="",
                tokens=total_tokens,
            )
            return File(path, [block])

        # The whole file is too large, split into blocks based on self.patterns
        blocks = re.split(self.patterns[0].start, code)

        if self.maximize_block_length:
            # Merge adjacent blocks back together to meet self.max_tokens
            grouper = CumulativeLengthGrouper(self.max_tokens, self._tokenizer)
            blocks = [
                '\n'.join(grp) for _, grp in groupby(blocks, key=grouper)
            ]

        block_id = 0
        for block in blocks:
            block_token_len = self._count_tokens(block)

            # The entire block is under the token length
            if block_token_len <= self.max_tokens:
                code_block = CodeBlock(
                    code=block,
                    path=path,
                    complete=True,
                    block_id=block_id,
                    segment_id=0,
                    language=self.language,
                    type="",
                    tokens=block_token_len,
                )
                components.append(code_block)
            # The whole block is too long, split into segments
            else:
                segments = self._split_block_into_segs(block)
                for segment_id, segment in enumerate(segments):
                    code_block = CodeBlock(
                        code=segment,
                        path=path,
                        complete=False,
                        block_id=block_id,
                        segment_id=segment_id,
                        language=self.language,
                        type="",
                        tokens=self._count_tokens(segment),
                    )
                    components.append(code_block)
            block_id += 1
        return File(path, components)

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

    def _count_tokens(self, code: str) -> int:
        """Count the number of tokens in the given code.

        Arguments:
            code: The code to count the number of tokens in.

        Returns:
            The number of tokens in the given code.
        """
        tokens = self._tokenizer.encode(code)
        return len(tokens)
