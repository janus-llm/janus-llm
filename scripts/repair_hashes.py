import argparse
import json
from collections import defaultdict
from pathlib import Path

from janus.language.block import JanusOutputObject, custom_hash

parser = argparse.ArgumentParser(
    description=("Fix nondeterministic hashes in existing Janus outputs.")
)
parser.add_argument("-i", "--indir", help="Directory containing JSON files.")
parser.add_argument("-o", "--outdir", help="Path to write output files")


def redefine_hash(node: JanusOutputObject):
    for child in node["outputs"]:
        redefine_hash(child)

    old_hash = node["metadata"]["hash"]
    obj_to_hash = (
        node["output"]
        if "output" in node
        else tuple(sorted(c["metadata"]["hash"] for c in node["outputs"]))
    )
    new_hash = custom_hash(obj_to_hash)

    if old_hash != new_hash:
        obj_str = str(obj_to_hash)
        if len(obj_str) > 25:
            obj_str = f"{obj_str[:10]} ... {obj_str[-10:]}"
        print(f"New hash: {repr(obj_str)} -> {new_hash}")
        node["metadata"]["hash"] = new_hash


if __name__ == "__main__":
    args = parser.parse_args()
    indir = Path(args.indir).expanduser()
    outdir = Path(args.outdir).expanduser()

    roots = ((p, json.loads(p.read_text())) for p in indir.rglob("*.json"))
    roots = ((p, n) for p, n in roots if not isinstance(n, list))
    for p, root in roots:
        print(f"Assessing {p}...")
        hash_counts = defaultdict(int)
        dupes = 0
        stack = [root]
        while stack:
            node = stack.pop()
            hash_counts[node["metadata"]["hash"]] += 1
            stack.extend(node["outputs"])
        dupes = [h for h, c in hash_counts.items() if c > 1]
        if dupes:
            print(f"Found {len(dupes)} duplicated hashes")

        print("Repairing hashes...")
        redefine_hash(root)

        print("Writing to file")
        out_path = outdir / p.relative_to(indir)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(root, indent=2))
