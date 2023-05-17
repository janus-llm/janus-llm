from dataclasses import dataclass
from pathlib import Path


@dataclass
class CodeBlock:
    """A base class for all language code blocks.

    Attributes:
        code: The code block.
        path: The path to the file containing the code block.
        complete: Whether or not the code block is complete.
        block_id: The ID of the code block.
        segment_id: The ID of the segment within the code block (if applicable).
        language: The language of the code block.
        type: The type of the code block ('function', 'module', etc.).
    """

    code: str
    path: Path
    complete: bool
    block_id: int
    segment_id: int
    language: str
    type: str
