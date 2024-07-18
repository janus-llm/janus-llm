"""A simple script to remove non-instructions from ALC files. The script can be
configured with arguments or a config file based on what the user wants to trim."""

import argparse
import json
import os
import re
from pathlib import Path


def strip_header_and_left(
    lines: list[str],
    header_end_str: str,
    left_margin_end_str: str,
) -> list[str]:
    """Remove the header and the left panel from the assembly sample"""

    esd_regex = re.compile(f".*{header_end_str}.*")

    header_end_index: int = [
        i for i, item in enumerate(lines) if re.search(esd_regex, item)
    ][0]

    left_content_end_column = lines[header_end_index].find(left_margin_end_str)
    hori_output_lines = lines[(header_end_index + 1) :]

    left_output_lines = [
        line[left_content_end_column + 5 :] for line in hori_output_lines
    ]
    return left_output_lines


def strip_addresses(lines: list[str], strip: int):
    """Strip the addresses which run down the right side of the assembly snippet"""

    stripped_lines = [line[:-strip] for line in lines]
    return stripped_lines


def strip_footer(lines: list[str]):
    """Strip the footer from the assembly snippet"""
    return NotImplementedError


def write_output(lines: list[str], output_file: Path):
    output_file.write_text("\n".join(lines))


def preproccess_assembly(
    lines: list[str], header_end_str: str, left_margin_end_str: str, addresses_column: int
):
    """Remove non-essential lines from an assembly snippet"""

    lines = strip_header_and_left(lines, header_end_str, left_margin_end_str)
    lines = strip_addresses(lines, addresses_column)
    # lines = strip_footer(lines)
    return lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process an assembly file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input_dir",
        type=Path,
        default=Path("samples"),
        help="Path to the input directory",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=Path,
        default=Path("output"),
        help="Path to the output directory",
    )
    parser.add_argument(
        "-e",
        "--trim_header",
        type=str,
        default="Loc  Object Code    Addr1 Addr2  Stmt   Source Statement",
        help="Indicator string for end of header",
    )
    parser.add_argument(
        "-a",
        "--trim_addresses",
        type=int,
        default=10,
        help="Number of characters to strip from addresses",
    )
    parser.add_argument(
        "-l",
        "--trim_left_margin",
        type=str,
        default="Stmt",
        help="Indicator string for end of left margin",
    )
    parser.add_argument("-c", "--config", type=str, help="Path to the config file")
    args = parser.parse_args()
    if args.config:
        with open(args.config) as config_file:
            config = json.load(config_file)
            input_dir = Path(config.get("input_dir", args.input_dir))
            output_dir = Path(config.get("output_dir", args.output_dir))
            trim_header = config.get("trim_header", args.trim_header)
            trim_addresses = config.get("trim_addresses", args.trim_addresses)
            trim_left_margin = config.get("trim_left_margin", args.trim_left_margin)
    else:
        input_dir = args.input_dir
        output_dir = args.output_dir
        trim_header = args.trim_header
        trim_addresses = args.trim_addresses
        trim_left_margin = args.trim_left_margin

    output_dir.mkdir(parents=True, exist_ok=True)
    for filename in os.listdir(input_dir):
        with open(os.path.join(input_dir, filename)) as f:
            input_lines = f.readlines()
        processed_lines = preproccess_assembly(
            input_lines, trim_header, trim_left_margin, trim_addresses
        )
        write_output(processed_lines, Path.joinpath(output_dir, filename))
