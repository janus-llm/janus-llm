import argparse
import json
import re
from pathlib import Path

from janus.utils.logger import create_logger

log = create_logger(__name__)


def process_comments_in_file(input_path: Path):
    data = json.loads(input_path.read_text())

    processed_str = data.get("input", "")
    generated_comments = data.get("output", {})

    comment_patterns = [
        (r"<BLOCK_COMMENT (\w{8})>", "<BLOCK_COMMENT {}>", "<BLOCK_COMMENT {}>"),
        (r"<INLINE_COMMENT (\w{8})>", "<INLINE_COMMENT {}>", "<INLINE_COMMENT {}>"),
        (r"<MODULE (\w{8})>", "<MODULE {}>", "<BLOCK_COMMENT {}>"),
    ]

    missing_comments = 0
    for pattern, find_template, repl_template in comment_patterns:
        matches = re.findall(pattern, processed_str)
        for comment_id in matches:
            find_tag = find_template.format(comment_id)
            repl_tag = repl_template.format(comment_id)
            if comment_id not in generated_comments:
                missing_comments += 1
            comment = generated_comments.get(comment_id, "[comment missing]")
            comment = comment.replace("\n", "\\n")
            processed_str = processed_str.replace(find_tag, f"{repl_tag} {comment}")

    if missing_comments:
        log.warning(f"{missing_comments} comments missing from {input_path}")

    processed_str = re.sub(r"\s*<JANUS_PARTITION>\s*\n", "\n", processed_str)
    return processed_str.strip("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Process comments in JSON files and output to MUMPS files with .m"
            " extension and formatted newlines."
        )
    )
    parser.add_argument("input_directory", help="Directory containing JSON files.")
    parser.add_argument("output_directory", help="Output directory for MUMPS files.")
    args = parser.parse_args()

    input_directory = Path(args.input_directory).expanduser()
    output_directory = Path(args.output_directory).expanduser()

    for input_path in input_directory.rglob("*.json"):
        modified_content = process_comments_in_file(input_path)
        output_path = output_directory / input_path.relative_to(
            input_directory
        ).with_suffix(".m")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(modified_content)
