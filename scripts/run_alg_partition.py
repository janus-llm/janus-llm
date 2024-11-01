import argparse
from pathlib import Path

from janus.language.combine import PartitionCombiner
from janus.language.naive import ChunkSplitter, get_flexible_ast, get_strict_ast
from janus.llm import load_model
from janus.utils.enums import LANGUAGES

parser = argparse.ArgumentParser(
    prog="Partition Code",
    description=("Partition code and write outputs with <JANUS_PARTITION> inserted"),
)

parser.add_argument(
    "-i",
    "--input-dir",
    type=str,
    required=True,
    help="The directory containing the source code to be partitioned",
)

parser.add_argument(
    "-o",
    "--output-dir",
    type=str,
    required=True,
    help="The directory to store the partitioned code",
)

parser.add_argument(
    "-l",
    "--language",
    type=str,
    default="mumps",
    help="The source code language",
)

parser.add_argument(
    "-L",
    "--llm",
    type=str,
    default="gpt-3.5-turbo",
    help="The model to use for tokenization",
)

args = parser.parse_args()
in_dir = Path(args.input_dir).expanduser()
out_dir = Path(args.output_dir).expanduser()

model, _, model_token_limit, _ = load_model(args.llm)
file_ext = LANGUAGES[args.language]["suffix"]
combiner = PartitionCombiner(args.language)

splitters = {
    "chunk": ChunkSplitter,
    "ast-flex": get_flexible_ast,
    "ast-strict": get_strict_ast,
}
token_limits = {
    "4k": int(4096 * 0.4),
    "8k": int(8192 * 0.4),
    "16k": int(16384 * 0.4),
    "32k": int(32000 * 0.4),
    "100k": int(100000 * 0.4),
    "128k": int(128000 * 0.4),
    "248k": int(248000 * 0.4),
}

for splitter_key, Splitter in splitters.items():
    for limit_key, token_limit in token_limits.items():
        splitter = Splitter(
            language=args.language,
            model=model,
            max_tokens=token_limit,
            prune_unprotected=False,
        )

        sub_out_dir = out_dir / splitter_key / limit_key
        sub_out_dir.mkdir(parents=True, exist_ok=True)
        for p in in_dir.rglob(f"**/*.{file_ext}"):
            root = splitter.split(p)
            combiner.combine(root)
            output_file = sub_out_dir / p.relative_to(in_dir)
            output_file.write_text(root.complete_text)
