import re
from dataclasses import dataclass

from ..utils.logger import create_logger

log = create_logger(__name__)


@dataclass
class Pattern:
    """A base class for all language patterns.

    Attributes:
        start_pattern: A regular expression pattern that matches the start of a
                       functional code block.
        end_pattern: A regular expression pattern that matches the end of a
                     functional code block.
        type: The type of the functional code block ('module', 'function', etc.).
    """

    start: re.Pattern
    end: re.Pattern
    type: str
