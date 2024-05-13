import argparse
import json
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


class LineInfo(object):
    def __init__(self, line):
        self.code = line
        self.comment = None
        self.comment_type = "inline"
        self.uuid = None

        idx = comment_start(line)
        if idx < 0:
            return

        comment = line[idx:]
        code_line = line[:idx]

        self.code = code_line
        self.comment = comment

    @property
    def has_comment(self) -> bool:
        return self.comment is not None

    @property
    def has_code(self) -> bool:
        return bool(self.code.strip(" ."))

    @property
    def is_label(self) -> bool:
        return self.code[0] not in "; "

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

    def string(self, placeholder: bool) -> str:
        if not self.has_comment:
            return self.code
        if self.is_separator or not placeholder:
            return self.code + self.comment
        return f"{self.code}; <{self.comment_type.upper()}_COMMENT {self.uuid}>"


def consolidate_block_comments(lines: Iterator[LineInfo]) -> Iterator[LineInfo]:
    working_group = []
    prefix = None
    for line in lines:
        # If the line has no comment, complete and yield any block comment in
        #  process, then yield the line
        if not line.has_comment:
            if working_group:
                yield from merge_comments(working_group)
                working_group = []
                prefix = None
            yield line

        # If the line has any non-indentation code, complete and yield any block
        #  comment in process, then either yield the line or start a new block
        #  comment (only if the line is a label)
        elif line.has_code:
            if working_group:
                yield from merge_comments(working_group)
                working_group = []
                prefix = None

            if line.is_label:
                working_group = [line]
                continue

            yield line

        # If the line is solely comment text (and indentation), either add it
        #  to the block comment in process, or start a new block comment
        else:
            if not working_group:
                working_group = [line]
                prefix = line.code
                continue

            # If there's a block comment in process but no prefix set, this is
            #  the first non-label comment
            if prefix is None:
                working_group.append(line)
                prefix = line.code

            # If this comment has the same indentation as the block comment in
            #  process, add it. Otherwise, start a new block comment
            if prefix == line.code:
                working_group.append(line)
            else:
                yield from merge_comments(working_group)
                working_group = [line]
                prefix = line.code

    if working_group:
        yield from merge_comments(working_group)


def merge_comments(lines: list[LineInfo]) -> Iterator[LineInfo]:
    # Peel any separators from the head and tail of the block
    prefix_seps = list(takewhile(lambda line: line.is_separator, lines))
    lines = list(dropwhile(lambda line: line.is_separator, lines))
    suffix_seps = list(takewhile(lambda line: line.is_separator, lines[::-1]))[::-1]
    lines = list(dropwhile(lambda line: line.is_separator, lines[::-1]))[::-1]

    yield from prefix_seps
    if lines:
        block = lines[0]
        block.comment = "\n".join(line.comment for line in lines)
        block.comment_type = "block"
        yield block
    yield from suffix_seps


def get_lines(code: str) -> list[LineInfo]:
    lines = (LineInfo(line) for line in code.split("\n"))
    lines = list(consolidate_block_comments(lines))

    # Assign unique IDs to lines
    seen_ids = set()
    for line in lines:
        while (cid := str(uuid.uuid4())[:8]) in seen_ids:
            pass
        seen_ids.add(cid)
        line.uuid = cid

    return lines


def process_directory(input_dir: Path, output_dir: Path):
    output_dir.mkdir(parents=True, exist_ok=True)

    obj = {}
    for input_file in input_dir.rglob("*.m"):
        output_file = output_dir / input_file.relative_to(input_dir)

        code = input_file.read_text()
        lines = get_lines(code)

        output_text = "\n".join(line.string(placeholder=True) for line in lines)
        output_file.write_text(output_text)
        comments = {
            line.uuid: line.comment
            for line in lines
            if line.has_comment and not line.is_separator
        }

        obj[input_file.name] = dict(
            original=code, processed=output_text, comments=comments
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
