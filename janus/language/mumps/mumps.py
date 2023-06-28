import re
from pathlib import Path
from typing import List, Tuple

import tiktoken

from ...utils.logger import create_logger
from ..block import CodeBlock
from ..splitter import Splitter
from .patterns import MumpsLabeledBlockPattern

log = create_logger(__name__)


class MumpsSplitter(Splitter):
    """A class for splitting MUMPS code into functional blocks to prompt with for
    transcoding.

    Attributes:
        patterns: A tuple of `Pattern`s to use for splitting Mumps code into
            functional blocks.
    """

    def __init__(
        self,
        patterns: Tuple[MumpsLabeledBlockPattern, ...] = (MumpsLabeledBlockPattern(),),
        max_tokens: int = 4096,
        model: str = "gpt-3.5-turbo",
    ) -> None:
        """Initialize a MumpsSplitter instance.

        Arguments:
            patterns: A tuple of `Pattern`s to use for splitting MUMPS code into
                functional blocks.
        """

        self.patterns: Tuple[MumpsLabeledBlockPattern, ...] = patterns
        # Divide max_tokens by 3 because we want to leave just as much space for the
        # prompt as for the translated code.
        self.max_tokens: int = max_tokens // 3
        # Using tiktoken as the tokenizer because that's what's recommended for OpenAI
        # models.
        self._tokenizer = tiktoken.encoding_for_model(model)
        self.language: str = "mumps"
        self.comment: str = ";"

    def _split(self, code: str, path: Path) -> List[CodeBlock]:
        """Split the given file into functional code blocks.

        Arguments:
            code: A string containing the code of the entire file to split
            path: The path to the code

        Returns:
            A File dataclass containing the path to the file and all of its code blocks
        """
        components: List[CodeBlock] = []

        # The whole file is one block
        if self._count_tokens(code) < self.max_tokens:
            block = CodeBlock(
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
            out_block = block
        else:
            blocks = re.split(self.patterns[0].start, code)
            for block in blocks:
                block_token_len = self._count_tokens(block)
                # The entire block is under the token length
                if block_token_len <= self.max_tokens:
                    code_block = CodeBlock(
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
                    components.append(code_block)
                # The whole block is too long, split into segments
                else:
                    segments = self._split_block_into_segs(block)
                    for segment_id, segment in enumerate(segments):
                        code_block = CodeBlock(
                            code=segment,
                            path=path,
                            complete=True,
                            start_line=0,
                            end_line=len(code.splitlines()),
                            depth=1,
                            id=segment_id,
                            children=[],
                            language=self.language,
                            type="file",
                            tokens=self._count_tokens(code),
                        )
                        components.append(code_block)
            out_block = CodeBlock(
                code=f"{self.comment} <<<child_0>>>\n",
                path=path,
                complete=True,
                start_line=0,
                end_line=len(code.splitlines()),
                depth=0,
                id=0,
                children=components,
                language=self.language,
                type="file",
                tokens=self._count_tokens(code),
            )
        return out_block

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
