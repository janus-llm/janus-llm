import argparse
import json
import random
import re
import uuid
from itertools import dropwhile, takewhile
from pathlib import Path
from typing import Iterator

from janus.language.block import CodeBlock
from janus.language.combine import Combiner
from janus.language.treesitter import TreeSitterSplitter

splitter = TreeSitterSplitter(language="ibmhlasm", max_tokens=float("inf"))

rnd = random.Random()


class CommentInfo(object):
    def __init__(self, block: CodeBlock):
        self.comment = block.text
        self.comment_start = block.start_byte
        self.comment_type = None
        self.prefix = ""
        self.uuid = str(uuid.UUID(int=rnd.getrandbits(128), version=4))[:8]

        # This is for the exhaustive inline comment generation case ONLY
        if "instruction" in block.node_type:
            self.comment_type = "inline"
            self.comment = ""
            self.placeholder = (
                f"{block.text} <{self.comment_type.upper()}_COMMENT {self.uuid}>"
            )
        else:
            if block.node_type == "comment":
                self.comment_type = "block"
                self.prefix = "* "
            elif block.node_type == "remark":
                self.comment_type = "inline"

            self.placeholder = (
                f"{self.prefix}<{self.comment_type.upper()}_COMMENT {self.uuid}>"
            )

    @property
    def is_separator(self) -> bool:
        return not re.sub(r"\W+", "", self.comment)

    def comment_text(self) -> str:
        if self.is_separator:
            return ""

        return " ".join(
            line.lstrip(" *").rstrip(" ")
            for line in self.comment.split("\n")
            if re.sub(r"\W+", "", line)
        )

    def placeholder(self) -> str:
        if self.is_separator:
            return self.comment
        return f"<{self.comment_type.upper()}_COMMENT {self.uuid}>"


def is_separator(comment: str) -> bool:
    return not re.sub(r"\W+", "", comment)


def merge_group(nodes: list[CodeBlock]) -> Iterator[CodeBlock]:
    yield from takewhile(lambda line: is_separator(line.text), nodes)
    nodes = list(dropwhile(lambda line: is_separator(line.text), nodes))

    prefix_seps = list(takewhile(lambda line: is_separator(line.text), nodes[::-1]))[::1]
    nodes = list(dropwhile(lambda line: is_separator(line.text), nodes[::-1]))[::-1]

    if nodes:
        merged = splitter.merge_nodes(nodes)
        merged.node_type = "comment"
        yield merged
    yield from prefix_seps


def merge_adjacent_comments(children: list[CodeBlock]) -> list[CodeBlock]:
    new_children: list[CodeBlock] = []
    run = []
    for child in sorted(children, key=lambda node: node.start_byte):
        if child.node_type == "comment":
            run.append(child)
            continue

        if len(run) == 1:
            new_children.append(run[0])
        elif len(run) > 1:
            new_children.extend(merge_group(run))
        new_children.append(child)
        run = []

    return new_children


def process(code: str) -> tuple[str, list[CommentInfo]]:
    root = splitter._get_ast(code)

    rnd.seed(code)

    comments = []
    stack = [root]
    while stack:
        node = stack.pop(0)

        if node.node_type in {"comment", "remark"}:
            if node.text is None:
                continue

            comment = CommentInfo(node)
            if comment.is_separator:
                continue

            comments.append(comment)
            node.text = comment.placeholder

        elif node.children:
            node.complete = False
            node.text = None
            node.children = merge_adjacent_comments(node.children)
            stack.extend(node.children)

    Combiner.combine(root)
    return root.complete_text, comments


def process_exhaustive(code: str) -> tuple[str, list[CommentInfo]]:
    root = splitter._get_ast(code)

    rnd.seed(code)

    comments = []
    stack = [root]

    while stack:
        node = stack.pop(0)

        if node.node_type == "comment":
            node.text = ""
        elif node.node_type == "remark":
            if node.text is None:
                continue

            comment = CommentInfo(node)
            if comment.is_separator:
                continue

            comments.append(comment)
            node.text = comment.placeholder

        elif (
            "instruction" in node.node_type
            and node.children
            and not node.children[-1].node_type == "remark"
        ):
            line = CommentInfo(node)
            comments.append(line)
            node.text = line.placeholder

        elif node.children:
            node.complete = False
            node.text = None
            node.children = merge_adjacent_comments(node.children)
            stack.extend(node.children)

    Combiner.combine(root)

    # Remove blank lines from the processed code
    processed_code_lines = root.complete_text.splitlines()
    non_blank_lines = [line for line in processed_code_lines if line.strip()]

    # Ensure comment tags do not exceed column 72
    adjusted_lines = []
    for line in non_blank_lines:
        if "<INLINE_COMMENT" in line and len(line) > 72:
            parts = line.split("<INLINE_COMMENT")
            base_line = parts[0].rstrip()
            comment_tag = "<INLINE_COMMENT" + parts[1]
            adjusted_lines.append(base_line)
            adjusted_lines.append(" " * 15 + comment_tag)
        else:
            adjusted_lines.append(line)

    processed_code = "\n".join(adjusted_lines)

    return processed_code, comments


if __name__ == "__main__":
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

    parser.add_argument(
        "--exhaustive",
        action="store_true",
        help="Whether to add comments to every line (rather than simply replacing"
        " existing comments)",
    )

    args = parser.parse_args()
    input_dir = Path(args.input_dir).expanduser()
    output_dir = Path(args.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)

    obj = {}
    for input_file in input_dir.rglob("*.asm"):
        output_file = output_dir / input_file.relative_to(input_dir)

        code = input_file.read_text()
        if args.exhaustive:
            processed_code, comments = process_exhaustive(code)
        else:
            processed_code, comments = process(code)

        obj[input_file.name] = dict(
            original=code,
            processed=processed_code,
            raw_comments={c.uuid: c.comment for c in comments},
            comment_texts={c.uuid: c.comment_text() for c in comments},
            comment_types={c.uuid: c.comment_type for c in comments},
            comment_starts={c.uuid: c.comment_start for c in comments},
            comment_prefixes={c.uuid: c.prefix for c in comments},
        )

        output_file.write_text(processed_code)

    (output_dir / "processed.json").write_text(json.dumps(obj, indent=2))
