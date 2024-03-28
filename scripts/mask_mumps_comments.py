import argparse
import json
import re
import uuid
from pathlib import Path

from janus.language.mumps import MumpsSplitter

block_comment_pat = re.compile(
    r"(?P<comment_start>^[ .]*;).*(?:\n(?P=comment_start).*)+(?=\n)",
    flags=re.MULTILINE,
)


def is_separator(comment: str) -> bool:
    return not re.sub(r"\W+", "", comment)


def block_comment_replacement(comment_match: re.Match) -> str:
    if is_separator(comment_match.group(0)):
        return comment_match.group(0)
    comment_start = comment_match.group("comment_start")
    return f"{comment_start} <BLOCK_COMMENT>"


def replace_block_comments(code: str) -> tuple[str, list[str]]:
    comments = [
        match.group(0)
        for match in re.finditer(block_comment_pat, code)
        if not is_separator(match.group(0))  # Exclude separators
    ]
    code = re.sub(
        block_comment_pat,
        block_comment_replacement,
        code,
    )
    return code, comments


def process(code: str) -> tuple[str, list[dict[str, str | int]]]:
    code, block_comments = replace_block_comments(code)

    processed_lines = []
    comments = {}
    for code_line in code.split("\n"):
        comment_start = MumpsSplitter.comment_start(code_line)
        has_comment = comment_start >= 0

        comment = None
        if has_comment:
            comment = code_line[comment_start:]
            code_line = code_line[:comment_start]

            # Ensure the comment isn't a separator
            if is_separator(comment):
                has_comment = False

        if not has_comment:
            processed_lines.append(code_line)
            continue

        comment_id = next(
            t for _ in range(1000) if (t := str(uuid.uuid4())[:8]) not in comments
        )

        if "; <BLOCK_COMMENT>" == comment:
            comment = block_comments.pop(0)
            placeholder = f"; <BLOCK_COMMENT {comment_id}>"
        else:
            placeholder = f"; <INLINE_COMMENT {comment_id}>"

        comments[comment_id] = comment
        processed_lines.append(code_line + placeholder)

    return "\n".join(processed_lines), comments


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
output_dir.mkdir(parents=True, exist_ok=True)

obj = {}
for input_file in input_dir.rglob("*.m"):
    output_file = output_dir / input_file.relative_to(input_dir)
    comment_file = output_file.with_suffix(".comments.txt")
    reference_file = output_file.with_suffix(".original.m")

    code = input_file.read_text()
    processed_code, comments = process(code)

    obj[input_file.name] = dict(
        original=code, processed=processed_code, comments=comments
    )

    # reference_file.write_text(code)
    output_file.write_text(processed_code)
    # comment_file.write_text("\n\n".join(comments))
    # exit()

(output_dir / "processed.json").write_text(json.dumps(obj, indent=2))
