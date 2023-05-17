import re
from pathlib import Path
from typing import List, Optional, Tuple

from .block import CodeBlock
from .pattern import Pattern


class Splitter:
    """A class for splitting code into functional blocks to prompt with for
    transcoding.
    """

    def __init__(self, patterns: Tuple[Pattern, ...], max_tokens: int = 4096) -> None:
        """Initialize a Splitter instance.

        Arguments:
            patterns: A tuple of `Pattern`s to use for splitting code into
                      functional blocks.
        """

        self.patterns: Tuple[Pattern, ...] = patterns
        self.max_tokens: int = max_tokens
        self.language: Optional[str] = None
        self.comment: Optional[str] = None

    def split(self, file: Path | str) -> Tuple[CodeBlock, ...]:
        path = Path(file)
        code = path.read_text()
        return self._split(code, path)

    def _split(self, code: str, path: Path) -> Tuple[CodeBlock, ...]:
        """Split the given file into functional code blocks.

        Arguments:
            file: The file to split into functional blocks.

        Returns:
            A tuple of functional blocks.
        """

        components: List[CodeBlock] = []
        current_component: str = ""
        token_count: int = 0
        in_block: bool = False
        segment_id: int = 0
        block_id: int = 0
        block_stack: List[CodeBlock] = []

        lines = code.splitlines()

        for line in lines:
            line = line.strip()

            if not line or line.startswith(self.comment):
                continue

            if in_block:
                current_component += line + "\n"
                match_end = block_stack[-1].search(line)
                if match_end:
                    block_stack.pop()
                    if not block_stack:
                        components.append(
                            CodeBlock(
                                code=current_component.strip(),
                                path=path,
                                complete=True,
                                block_id=block_id,
                                segment_id=segment_id,
                                language=self.language,
                                type="",
                                tokens=self._count_tokens(current_component.strip()),
                            )
                        )
                        current_component = ""
                        token_count = 0
                        segment_id = 0
                        in_block = False
                continue

            if self._count_tokens(current_component) > self.max_tokens:
                if token_count > 0:
                    components.append(
                        CodeBlock(
                            code=current_component.strip(),
                            path=path,
                            complete=False,
                            block_id=block_id,
                            segment_id=segment_id,
                            language=self.language,
                            type="",
                            tokens=self._count_tokens(current_component.strip()),
                        )
                    )
                    current_component = ""
                    token_count = 0
                    segment_id += 1

            if not in_block:
                match_start = False
                for pattern in self.patterns:
                    if pattern.start.search(line) is not None:
                        match_start = True
                        block_pattern = pattern
                if match_start:
                    if current_component:
                        components.append(
                            CodeBlock(
                                code=current_component.strip(),
                                path=path,
                                complete=False,
                                block_id=block_id,
                                segment_id=segment_id,
                                language=self.language,
                                type="",
                                tokens=self._count_tokens(current_component.strip()),
                            )
                        )
                        current_component = ""
                        token_count = 0
                        segment_id += 1
                    in_block = True
                    current_component += line + "\n"
                    block_id += 1
                    block_stack.append(block_pattern.end)
                else:
                    current_component += line + "\n"

        if current_component:
            components.append(
                CodeBlock(
                    code=current_component.strip(),
                    path=path,
                    complete=False,
                    block_id=block_id,
                    segment_id=segment_id,
                    language=self.language,
                    type="",
                    tokens=self._count_tokens(current_component.strip()),
                )
            )

        return components

    def _count_tokens(self, code: str) -> int:
        """Count the number of tokens in the given code.

        Arguments:
            code: The code to count the number of tokens in.

        Returns:
            The number of tokens in the given code.
        """

        code = re.sub(r'("(?:""|[^"])*")', "", code)  # Remove string literals
        tokens = re.split(r"[^\w]+", code)  # Split by non-word characters
        tokens = [token for token in tokens if token]  # Remove empty tokens
        return len(tokens)
