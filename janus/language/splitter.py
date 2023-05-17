from pathlib import Path
from typing import List, Optional, Tuple

from .pattern import Pattern
from .block import CodeBlock


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
            tokens = line.strip().split()
            line_token_count = len(tokens)
            total_token_count = token_count + line_token_count

            if in_block:
                current_component += line + "\n"
                match_end = block_stack[-1].search(line)
                if match_end:
                    block_stack.pop()
                    if not block_stack:
                        components.append(
                            CodeBlock(
                                code=current_component.strip(),
                                path="",
                                complete=True,
                                block_id=block_id,
                                segment_id=segment_id,
                                language="Fortran",
                                type="",
                            )
                        )
                        current_component = ""
                        token_count = 0
                        segment_id = 0
                        in_block = False
                continue

            if total_token_count > self.max_tokens:
                if token_count > 0:
                    components.append(
                        CodeBlock(
                            code=current_component.strip(),
                            path="",
                            complete=False,
                            block_id=block_id,
                            segment_id=segment_id,
                            language="Fortran",
                            type="",
                        )
                    )
                    current_component = ""
                    token_count = 0
                    segment_id += 1

            if not in_block:
                for pattern in self.patterns:
                    match_start = pattern.start.search(line)
                    if match_start:
                        in_block = True
                        current_component += line + "\n"
                        token_count += line_token_count
                        block_id += 1
                        block_stack.append(pattern.end)
                        break

            token_count += line_token_count

        if current_component:
            components.append(
                CodeBlock(
                    code=current_component.strip(),
                    path="",
                    complete=False,
                    block_id=block_id,
                    segment_id=segment_id,
                    language="Fortran",
                    type="",
                )
            )

        return components
