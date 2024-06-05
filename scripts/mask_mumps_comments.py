from __future__ import annotations

import argparse
import json
import random
import re
import uuid
from itertools import dropwhile, takewhile
from pathlib import Path
from typing import Iterator


def comment_start(line: str) -> int:
    first_semicolon = line.find(";")
    if first_semicolon < 0:
        return first_semicolon

    # In mumps, quotes are escaped by doubling them (""). Single quote
    #  characters are logical not operators, not quotes
    n_quotes = line[:first_semicolon].replace('""', "").count('"')

    # If the number of quotes prior to the first semicolon is even, then
    #  that semicolon is not part of a quote (and therefore starts a comment)
    if n_quotes % 2 == 0:
        return first_semicolon

    last_semicolon = first_semicolon
    while (next_semicolon := line.find(";", last_semicolon + 1)) > 0:
        n_quotes = line[last_semicolon:next_semicolon].replace('""', "").count('"')

        # If the number of quotes in this chunk is odd, the total number
        #  of them up to this point is even, and the next semicolon begins
        #  the comment
        if n_quotes % 2:
            return next_semicolon

        last_semicolon = next_semicolon

    return -1


class CommentInfo(object):
    def __init__(self, line: str, start_byte: int):
        self.code = line
        self.comment = None
        self.comment_offset = None
        self.comment_start = None
        self.comment_type = None
        self.comment_prefix = None

        self.line_start = start_byte
        self.uuid = None

        idx = comment_start(line)
        if idx < 0:
            return

        self.code = line[:idx]
        self.comment = line[idx:]
        self.comment_offset = idx
        self.comment_start = self.line_start + self.comment_offset

        if self.is_label:
            self.comment_type = "block"
            self.comment_prefix = " ; "
        elif self.is_separator:
            self.comment_type = "separator"
            self.comment_prefix = ";"
        elif self.has_code:
            self.comment_type = "inline"
            self.comment_prefix = ";"
        else:
            self.comment_type = "block"
            self.comment_prefix = self.code + "; "

    @property
    def has_comment(self) -> bool:
        return self.comment is not None

    @property
    def has_code(self) -> bool:
        return bool(self.code.strip(" ."))

    @property
    def is_label(self) -> bool:
        return self.code and self.code[0] not in "; "

    @property
    def is_separator(self) -> bool:
        return not re.sub(r"\W+", "", self.comment)

    @property
    def placeholder(self) -> str:
        if not self.has_comment:
            return self.code
        if self.is_separator:
            return self.code + self.comment
        return f"{self.code}; <{self.comment_type.upper()}_COMMENT {self.uuid}>"

    def append(self, other: CommentInfo):
        self.comment += "\n" + other.code + other.comment

    def comment_text(self) -> str:
        if self.is_separator or not self.has_comment:
            return ""

        # Remove any prefixes (indentation and comment delimiters) and trailing
        #  space from each non-separator line, and merge them into a single string
        return " ".join(
            line.lstrip(" .;").rstrip(" ")
            for line in self.comment.split("\n")
            if re.sub(r"\W+", "", line)
        )

    def string(self, placeholder: bool) -> str:
        if not self.has_comment:
            return self.code
        if self.is_separator or not placeholder:
            return self.code + self.comment
        return f"{self.code}; <{self.comment_type.upper()}_COMMENT {self.uuid}>"


def consolidate_block_comments(lines: Iterator[CommentInfo]) -> Iterator[CommentInfo]:
    working_group = []
    prefix = None
    is_subroutine_start = False
    for line in lines:
        # If the line has no comment, complete and yield any block comment in
        #  process, then yield the line
        if not line.has_comment:
            if working_group:
                yield from merge_comments(working_group, is_subroutine_start)
                working_group = []
                prefix = None
            yield line
            is_subroutine_start = line.is_label

        # If the line has any non-indentation code, complete and yield any block
        #  comment in process, then either yield the line or start a new block
        #  comment (only if the line is a label)
        elif line.has_code:
            if working_group:
                yield from merge_comments(working_group, is_subroutine_start)
                working_group = []
                prefix = None

            if line.is_label:
                working_group = [line]
                is_subroutine_start = True
            else:
                yield line
                is_subroutine_start = False

        # If the line is solely comment text (and indentation), either add it
        #  to the block comment in process, or start a new block comment
        else:
            # If there's no prefix on the working block, then either this is the
            #  first line of a block comment, or it's the second line of a
            #  subroutine block comment. Either way, continue the block.
            # If there is a prefix and it's different than this comment's
            #  indentation, then yield the working block and start a new one
            if prefix is not None and prefix != line.code:
                yield from merge_comments(working_group, is_subroutine_start)
                working_group = []
                is_subroutine_start = False

            working_group.append(line)
            prefix = line.code

    if working_group:
        yield from merge_comments(working_group, is_subroutine_start)


def merge_comments(
    lines: list[CommentInfo], is_subroutine_start: bool = False
) -> Iterator[CommentInfo]:
    # Peel any separators from the head the block (unless it starts a subroutine)
    if not is_subroutine_start:
        yield from takewhile(lambda line: line.is_separator, lines)
        lines = list(dropwhile(lambda line: line.is_separator, lines))

    # Peel any separators from the tail of the block
    suffix_seps = list(takewhile(lambda line: line.is_separator, lines[::-1]))[::-1]
    lines = list(dropwhile(lambda line: line.is_separator, lines[::-1]))[::-1]

    if lines:
        block = lines[0]
        for line in lines[1:]:
            block.append(line)
        yield block
    yield from suffix_seps


def get_comments(code: str) -> list[CommentInfo]:
    comments = []
    start_byte = 0
    for line in code.split("\n"):
        comments.append(CommentInfo(line, start_byte))
        start_byte += len(line) + 1
    comments = list(consolidate_block_comments(comments))

    # Assign unique IDs to lines
    rnd = random.Random()
    rnd.seed(code)
    for comment in comments:
        if comment.has_comment and not comment.is_separator:
            comment.uuid = str(uuid.UUID(int=rnd.getrandbits(128), version=4))[:8]

    return comments


def process_directory(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    obj = {}
    for input_file in input_dir.rglob("*.m"):
        output_file = output_dir / input_file.relative_to(input_dir)

        code = input_file.read_text()
        lines = get_comments(code)
        comment_lines = [
            line for line in lines if line.has_comment and not line.is_separator
        ]

        output_text = "\n".join(line.string(placeholder=True) for line in lines)
        output_file.write_text(output_text)
        raw_comments = {line.uuid: line.comment for line in comment_lines}
        comment_texts = {line.uuid: line.comment_text() for line in comment_lines}
        comment_types = {line.uuid: line.comment_type.upper() for line in comment_lines}
        comment_starts = {line.uuid: line.comment_start for line in comment_lines}
        comment_prefixes = {line.uuid: line.comment_prefix for line in comment_lines}

        obj[input_file.name] = dict(
            original=code,
            processed=output_text,
            raw_comments=raw_comments,
            comment_texts=comment_texts,
            comment_types=comment_types,
            comment_starts=comment_starts,
            comment_prefixes=comment_prefixes,
        )

    (output_dir / "processed.json").write_text(json.dumps(obj, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Mask MUMPS Comments",
        description="Replace MUMPS comments with numbers, to be used in MadLibs-style"
        " automatic documentation evaluation.",
    )

    parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="The directory containing the source code to be processed",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="The directory to store the processed code",
    )

    args = parser.parse_args()
    input_dir = Path(args.input_dir).expanduser()
    output_dir = Path(args.output_dir).expanduser()

    process_directory(input_dir, output_dir)
