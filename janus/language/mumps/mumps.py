from typing import Tuple

from ...utils.logger import create_logger
from ..pattern import Pattern
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
        patterns: Tuple[Pattern, ...] = (
            MumpsLabeledBlockPattern()
        ),
        max_tokens: int = 4096,
    ) -> None:
        """Initialize a MumpsSplitter instance.

        Arguments:
            patterns: A tuple of `Pattern`s to use for splitting MUMPS code into
                functional blocks.
        """

        super().__init__(patterns, max_tokens)
        self.language: str = "mumps"
        self.comment: str = ";"
