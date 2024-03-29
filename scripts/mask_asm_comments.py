import argparse
import json
import re
import uuid
from pathlib import Path

from janus.language.block import CodeBlock
from janus.language.combine import Combiner
from janus.language.treesitter import TreeSitterSplitter

splitter = TreeSitterSplitter(language="ibmhlasm", max_tokens=float("inf"))


def is_separator(comment: str) -> bool:
    return not re.sub(r"\W+", "", comment)


def merge_adjacent_comments(children: list[CodeBlock]) -> list[CodeBlock]:
    new_children: list[CodeBlock] = []
    run = []
    for child in children:
        if child.node_type == "comment":
            run.append(child)
            continue

        if len(run) == 1:
            new_children.append(run[0])
        elif len(run) > 1:
            merged = splitter.merge_nodes(run)
            merged.node_type = "comment"
            new_children.append(merged)
        run = []

        new_children.append(child)
    return new_children


def process(code: str) -> tuple[str, list[dict[str, str | int]]]:
    root = splitter._get_ast(code)

    comments = {}
    stack = [root]
    while stack:
        node = stack.pop()

        if node.node_type in {"comment", "remark"}:
            if is_separator(node.text):
                node.text = ""
                continue

            comment_id = next(
                t for _ in range(1000) if (t := str(uuid.uuid4())[:8]) not in comments
            )
            comments[comment_id] = node.text
            if node.node_type == "comment":
                node.text = f"* <BLOCK_COMMENT {comment_id}>"
            else:
                node.text = f"<INLINE_COMMENT {comment_id}>"

        elif node.children:
            node.complete = False
            node.text = None
            node.children = merge_adjacent_comments(node.children)
            stack.extend(node.children)

    Combiner.combine(root)
    return root.complete_text, comments


parser = argparse.ArgumentParser(
    prog="Mask ASM Comments",
    description="Replace ASM comments with placeholders, to be used in "
    "MadLibs-style automatic documentation evaluation.",
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
for input_file in input_dir.rglob("*.asm"):
    output_file = output_dir / input_file.relative_to(input_dir)

    code = input_file.read_text()
    processed_code, comments = process(code)

    obj[input_file.name] = dict(
        original=code, processed=processed_code, comments=comments
    )

    output_file.write_text(processed_code)

(output_dir / "processed.json").write_text(json.dumps(obj, indent=2))
