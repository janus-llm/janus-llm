import re
from dataclasses import dataclass

from ...utils.logger import create_logger
from ..pattern import Pattern

log = create_logger(__name__)


@dataclass
class FortranSubroutinePattern(Pattern):
    """A pattern for matching Fortran subroutines.

    Attributes:
        start_pattern: A regular expression pattern that matches the start of a
                       Fortran subroutine.
        end_pattern: A regular expression pattern that matches the end of a
                     Fortran subroutine.
        type: The type of the functional code block ('module', 'function', etc.).
    """

    start: re.Pattern = re.compile(r"(?<!\n)\n(?= *SUBROUTINE)", re.IGNORECASE)
    end: re.Pattern = re.compile(r"END\s+SUBROUTINE", re.IGNORECASE)
    type: str = "subroutine"


@dataclass
class FortranFunctionPattern(Pattern):
    """A pattern for matching Fortran functions.

    Attributes:
        start_pattern: A regular expression pattern that matches the start of a
                       Fortran function, excluding the 'END FUNCTION' line.
        end_pattern: A regular expression pattern that matches the end of a
                     Fortran function.
        type: The type of the functional code block ('module', 'function', etc.).
    """

    start: re.Pattern = re.compile(
        r"FUNCTION\s+(\w+)(?!\s*END\s+FUNCTION)", re.IGNORECASE
    )
    end: re.Pattern = re.compile(r"END\s+FUNCTION", re.IGNORECASE)
    type: str = "function"


@dataclass
class FortranIfPattern(Pattern):
    """A pattern for matching Fortran IF blocks.

    Attributes:
        start_pattern: A regular expression pattern that matches the start of a
                       Fortran IF block.
        end_pattern: A regular expression pattern that matches the end of a
                     Fortran IF block.
        type: The type of the functional code block ('if', 'do', etc.).
    """

    start: re.Pattern = re.compile(r"^\s*IF", re.IGNORECASE)
    end: re.Pattern = re.compile(r"^\s*ENDIF", re.IGNORECASE)
    type: str = "if"


@dataclass
class FortranDoPattern(Pattern):
    """A pattern for matching Fortran DO blocks.

    Attributes:
        start_pattern: A regular expression pattern that matches the start of a
                       Fortran DO block.
        end_pattern: A regular expression pattern that matches the end of a
                     Fortran DO block.
        type: The type of the functional code block ('if', 'do', etc.).
    """

    start: re.Pattern = re.compile(r"^\s*DO", re.IGNORECASE)
    end: re.Pattern = re.compile(r"^\s*ENDDO", re.IGNORECASE)
    type: str = "do"


@dataclass
class FortranModulePattern(Pattern):
    """A pattern for matching Fortran modules.

    Attributes:
        start_pattern: A regular expression pattern that matches the start of a
                       Fortran module, excluding the 'END MODULE' line.
        end_pattern: A regular expression pattern that matches the end of a
                     Fortran module.
        type: The type of the functional code block ('module', 'function', etc.).
    """

    start: re.Pattern = re.compile(r"MODULE\s+(\w+)(?!\s*END\s+MODULE)", re.IGNORECASE)
    end: re.Pattern = re.compile(r"END\s+MODULE", re.IGNORECASE)
    type: str = "module"


@dataclass
class FortranProgramPattern(Pattern):
    """A pattern for matching Fortran programs.

    Attributes:
        start_pattern: A regular expression pattern that matches the start of a
                       Fortran program, excluding the 'END PROGRAM' line.
        end_pattern: A regular expression pattern that matches the end of a
                     Fortran program.
        type: The type of the functional code block ('module', 'function', etc.).
    """

    start: re.Pattern = re.compile(r"PROGRAM\s+(\w+)(?!\s*END\s+PROGRAM)", re.IGNORECASE)
    end: re.Pattern = re.compile(r"END\s+PROGRAM", re.IGNORECASE)
    type: str = "program"


@dataclass
class FortranBlockDataPattern(Pattern):
    """A pattern for matching Fortran block data.

    Attributes:
        start_pattern: A regular expression pattern that matches the start of a
                       Fortran block data, excluding the 'END BLOCK DATA' line.
        end_pattern: A regular expression pattern that matches the end of a
                     Fortran block data.
        type: The type of the functional code block ('module', 'function', etc.).
    """

    start: re.Pattern = re.compile(
        r"BLOCK\s+DATA\s+(\w+)(?!\s*END\s+BLOCK\s+DATA)", re.IGNORECASE
    )
    end: re.Pattern = re.compile(r"END\s+BLOCK\s+DATA", re.IGNORECASE)
    type: str = "block data"


@dataclass
class FortranInterfacePattern(Pattern):
    """A pattern for matching Fortran interfaces.

    Attributes:
        start_pattern: A regular expression pattern that matches the start of a
                       Fortran interface, excluding the 'END INTERFACE' line.
        end_pattern: A regular expression pattern that matches the end of a
                     Fortran interface.
        type: The type of the functional code block ('module', 'function', etc.).
    """

    start: re.Pattern = re.compile(
        r"INTERFACE\s+(\w+)(?!\s*END\s+INTERFACE)", re.IGNORECASE
    )
    end: re.Pattern = re.compile(r"END\s+INTERFACE", re.IGNORECASE)
    type: str = "interface"
