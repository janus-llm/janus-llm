"""
Script for ASM files to place comments
inline at tags, with support for specifying
an output directory and preserving the
file structure of the input directory.

In: Directory to json files that have 'code' + 'comments'
Out: Same directory structure in the output directory,
with ASM files that have comments appended.
"""
import json
import os
import re

import click


@click.command()
@click.argument("input_dir", type=click.Path(exists=True))
@click.argument("output_dir", type=click.Path())
def process_directory(input_dir, output_dir):
    # Define patterns and templates for locating and replacing tags.
    comment_pattern = re.compile(r"(<(BLOCK_COMMENT|INLINE_COMMENT)\s+([a-f0-9]+)>)")

    def process_json_file(input_file, output_base_dir):
        with open(input_file, "r") as file:
            data = json.load(file)

        # Extract "processed" and "generated_comment_texts" from the JSON structure
        processed_text = data.get("processed", "")
        comment_texts = data.get("generated_comment_texts", {})

        # Append the comment after each <BLOCK_COMMENT id> or <INLINE_COMMENT id>
        def append_comment(match):
            full_marker = match.group(1)
            comment_id = match.group(3)
            comment = comment_texts.get(comment_id, "")

            if comment:
                return f"{full_marker} {comment}"
            else:
                return full_marker

        # Replace each <BLOCK_COMMENT id> & <INLINE_COMMENT id> with the appended comment
        processed_text_with_comments = comment_pattern.sub(append_comment, processed_text)

        # Prepare the output file path while maintaining the directory structure
        relative_input_path = os.path.relpath(input_file, input_dir)
        output_subdir = os.path.join(
            output_base_dir, os.path.dirname(relative_input_path)
        )
        os.makedirs(output_subdir, exist_ok=True)

        output_file_path = os.path.join(
            output_subdir, f"{os.path.basename(input_file).replace('.json', '.asm')}"
        )
        with open(output_file_path, "w") as output_file:
            output_file.write(processed_text_with_comments)
            print(f"Created: {output_file_path}")

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                input_file_path = os.path.join(root, file)
                process_json_file(input_file_path, output_dir)


if __name__ == "__main__":
    process_directory()
