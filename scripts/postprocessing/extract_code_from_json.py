import argparse
import json
from pathlib import Path

from janus.utils.enums import LANGUAGES

parser = argparse.ArgumentParser(description=("Classify the language of generated text."))
parser.add_argument("-i", "--indir", help="Directory containing JSON files.")
parser.add_argument("-o", "--outdir", help="Path to write output files")


if __name__ == "__main__":
    args = parser.parse_args()
    indir = Path(args.indir).expanduser()
    outdir = Path(args.outdir).expanduser()

    for fin in indir.rglob("*.json"):
        obj = json.loads(fin.read_text())
        lang = obj["metadata"]["language"]
        ext = "txt"
        if lang in LANGUAGES:
            ext = LANGUAGES[lang]["suffixes"][0]

        relpath = fin.relative_to(indir)
        fout = (outdir / relpath).with_suffix(f".{ext}")

        root = json.loads(fin.read_text())
        queue = [root]
        chunks = []
        while queue:
            node = queue.pop(0)
            if "output" in node:
                chunks.append(node["output"])
            else:
                queue = node["outputs"] + queue

        if lang == "json":
            objs = [json.loads(s) for s in chunks]
            if all(isinstance(x, list) for x in objs):
                obj = sum(objs, start=[])

            elif all(isinstance(x, dict) for x in objs):
                obj = {}
                for x in objs:
                    obj.update(x)

            code = json.dumps(obj, indent=4)

        else:
            code = "\n".join(chunks)

        fout.parent.mkdir(parents=True, exist_ok=True)
        fout.write_text(code)
