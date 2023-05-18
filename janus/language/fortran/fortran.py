from typing import Tuple

from ...utils.logger import create_logger
from ..pattern import Pattern
from ..splitter import Splitter
from .patterns import FortranFunctionPattern, FortranSubroutinePattern

log = create_logger(__name__)


class FortranSplitter(Splitter):
    """A class for splitting Fortran code into functional blocks to prompt with for
    transcoding.

    Attributes:
        patterns: A tuple of `Pattern`s to use for splitting Fortran code into
                  functional blocks.
    """

    def __init__(
        self,
        patterns: Tuple[Pattern, ...] = (
            FortranFunctionPattern(),
            # FortranIfPattern(),
            # FortranDoPattern(),
            # FortranModulePattern(),
            # FortranProgramPattern(),
            FortranSubroutinePattern(),
        ),
        max_tokens: int = 4096,
    ) -> None:
        """Initialize a Fortran instance.

        Arguments:
            patterns: A tuple of `Pattern`s to use for splitting Fortran code into
                      functional blocks.
        """

        super().__init__(patterns, max_tokens)
        self.language: str = "fortran"
        self.comment: str = "!"
