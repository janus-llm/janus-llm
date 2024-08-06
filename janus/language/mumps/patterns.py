import re
from dataclasses import dataclass

from janus.utils.logger import create_logger

log = create_logger(__name__)

# From slides 52-54 of "A Quick Introduction to the Mumps Programming Language,
#  by Kevin C. O'Kane, University of Northern Iowa
# https://www.youtube.com/channel/UC5oHS9h-prWeBrBNzXm8rYA
MUMPS_COMMANDS = [
    "break",
    "b",
    "close",
    "c",
    "database",
    "do",
    "d",
    "else",
    "e",
    "for",
    "f",
    "goto",
    "g",
    "halt",
    "h",
    "hang",
    "html",
    "if",
    "i",
    "job",
    "j",
    "lock",
    "l",
    "kill",
    "k",
    "merge",
    "m",
    "new",
    "n",
    "open",
    "o",
    "quit",
    "q",
    "read",
    "r",
    "set",
    "s",
    "shell",
    "sql",
    "tcommit",
    "tc",
    "trestart",
    "tre",
    "trollback",
    "tro",
    "tstart",
    "use",
    "u",
    "view",
    "v",
    "write",
    "w",
    "xecute",
    "x",
    "z.+",
]

# Regex definitions
comment = r"[\t ]*;.*\n"
optional_inline_comment = "[\t ]+(?:;.*)?\n|[\t ]*\n"

# Labels start on column 1
label_start = r"[^ \t;$]"
routine_start = rf"((?<!\n)\n(?={label_start}))"
routine_end = rf"[ \t](?:Q(?:UIT)?|H(?:ALT)?){optional_inline_comment}"

# This is meant to split routines such that comments preceding it are included
#  r'\n(?=(?:[\t ]*;.*\n)*[^ \t;$])'
# However, it splits after every comment line (for comments that precede a routine)
# The way to fix this would be a negative look-behind:
#    ++++++++++++++++
#  r'(?<![\t ]*;.*\n)\n(?=(?:[\t ]*;.*\n)*[^ \t;$])'
# But this doesn't work because it's not fixed-width
# neg_lookback = fr'(?<!{comment_line})'
# routine_start_including_comments = fr"{neg_lookback}\n(?=(?:{comment})*{label_start})"


@dataclass
class MumpsLabeledBlockPattern:
    """A pattern for matching MUMPS labeled blocks.

    Attributes:
        start: A regular expression pattern that matches the label at the
            beginning of a MUMPS block (typically a routine).
        end: A regular expression pattern that matches the end of a MUMPS block.
        type: The type of the functional code block ('module', 'function', etc.).
    """

    start: re.Pattern = re.compile(routine_start)
    end: re.Pattern = re.compile(rf"(?<!\n)\n(?={routine_end})", re.IGNORECASE)
    type: str = "labeled_block"
