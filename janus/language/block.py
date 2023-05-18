from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass
class CodeBlock:
    """A class that represents a functional block of code.

    Attributes:
        code: The code block.
        path: The path to the file containing the code block.
        complete: Whether or not the code block is complete.
        block_id: The ID of the code block.
        segment_id: The ID of the segment within the code block (if applicable).
        language: The language of the code block.
        type: The type of the code block ('function', 'module', etc.).
        tokens: The number of tokens in the code block.
    """

    code: str
    path: Path
    complete: bool
    block_id: int
    segment_id: int
    language: str
    type: str
    tokens: int


@dataclass
class TranslatedCodeBlock:
    """A class that represents the translated functional block of code.

    Attributes:
        code: The code block.
        path: The path to the file containing the code block.
        complete: Whether or not the code block is complete.
        block_id: The ID of the code block.
        segment_id: The ID of the segment within the code block (if applicable).
        language: The language of the code block.
        type: The type of the code block ('function', 'module', etc.).
        tokens: The number of tokens in the code block.
        original: The original code block.
    """

    code: str
    path: Path
    complete: bool
    block_id: int
    segment_id: int
    language: str
    type: str
    tokens: int
    original: CodeBlock


@dataclass
class File:
    """A class that represents a file made up of functional blocks of code.

    Attributes:
        path: The path to the file.
        blocks: The functional blocks of code in the file.
    """

    path: Path
    blocks: Tuple[CodeBlock, ...]
