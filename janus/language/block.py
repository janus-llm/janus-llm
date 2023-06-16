from dataclasses import dataclass
from pathlib import Path
from typing import ForwardRef, Tuple

from ..utils.logger import create_logger
from .node import NodeType

log = create_logger(__name__)


@dataclass
class CodeBlock:
    """A class that represents a functional block of code.

    Attributes:
        code: The code block.
        path: The path to the file containing the code block.
        complete: Whether or not the code block is complete. If it isn't complete, it
                  should have children compoenents. This means that this code block has
                  missing sections inside of it that are in its children.
        parent_id: The ID of the parent code block (if applicable).
        start_line: The line number of the first line of the code block.
        end_line: The line number of the last line of the code block.
        children: A tuple of child code blocks.
        language: The language of the code block.
        type: The type of the code block ('function', 'module', etc.). Defined in the
              language-specific modules.
        tokens: The number of tokens in the code block.
    """

    code: str
    path: Path
    complete: bool
    parent_id: int
    start_line: int
    end_line: int
    language: str
    type: NodeType
    tokens: int
    children: Tuple[ForwardRef("CodeBlock")]


@dataclass
class TranslatedCodeBlock:
    """A class that represents the translated functional block of code.

    Attributes:
        code: The code block.
        path: The path to the file containing the code block.
        complete: Whether or not the code block is complete. If it isn't complete, it
                  should have children compoenents. This means that this code block has
                  missing sections inside of it that are in its children.
        parent_id: The ID of the parent code block (if applicable).
        start_line: The line number of the first line of the code block.
        end_line: The line number of the last line of the code block.
        children: A tuple of child translated code blocks.
        language: The language of the code block.
        type: The type of the code block ('function', 'module', etc.).
        tokens: The number of tokens in the code block.
        original: The original code block.
        cost: The total cost to translate the original code block.
    """

    code: str
    path: Path
    complete: bool
    parent_id: int
    start_line: int
    end_line: int
    children: Tuple[ForwardRef("TranslatedCodeBlock")]
    language: str
    type: str
    tokens: int
    original: CodeBlock
    cost: float


@dataclass
class File:
    """A class that represents a file made up of functional blocks of code.

    Attributes:
        path: The path to the file.
        blocks: The functional blocks of code in the file.
    """

    path: Path
    blocks: Tuple[CodeBlock, ...]
