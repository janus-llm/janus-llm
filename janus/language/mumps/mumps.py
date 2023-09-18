import re
from pathlib import Path
from typing import List, Tuple

from langchain.schema.language_model import BaseLanguageModel

from ...utils.logger import create_logger
from ..block import CodeBlock
from ..combine import Combiner
from ..splitter import Splitter
from .patterns import MumpsLabeledBlockPattern

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

    def __init__(
        self,
        model: BaseLanguageModel,
        patterns: Tuple[MumpsLabeledBlockPattern, ...] = (MumpsLabeledBlockPattern(),),
        max_tokens: int = 4096,
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
        self.model = model
        self.language: str = "mumps"
        self.comment: str = ";"

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
        if block_length < self.max_tokens:
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

        seen_ids = set()

        def id_gen():
            block_id = f"<<<child_{len(seen_ids)}>>>"
            seen_ids.add(block_id)
            return block_id

        blocks: List[CodeBlock] = []
        start_line = 0
        for i, block in enumerate(re.split(self.patterns[0].start, code)):
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
                    tokens=self._count_tokens(block),
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
            tokens=self._count_tokens(code),
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
