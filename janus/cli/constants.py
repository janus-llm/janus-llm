import json
from pathlib import Path

import janus.refiners.format
import janus.refiners.refiner
import janus.refiners.uml

homedir = Path.home().expanduser()

janus_dir = homedir / ".janus"
if not janus_dir.exists():
    janus_dir.mkdir(parents=True)

db_file = janus_dir / ".db"
if not db_file.exists():
    with open(db_file, "w") as f:
        f.write(str(janus_dir / "chroma.db"))

with open(db_file, "r") as f:
    db_loc = f.read()

collections_config_file = Path(db_loc) / "collections.json"


def get_subclasses(cls):
    return set(cls.__subclasses__()).union(
        set(s for c in cls.__subclasses__() for s in get_subclasses(c))
    )


REFINER_TYPES = get_subclasses(janus.refiners.refiner.JanusRefiner).union(
    {janus.refiners.refiner.JanusRefiner}
)
REFINERS = {r.__name__: r for r in REFINER_TYPES}

CONVERTER_TYPES = get_subclasses(janus.converter.converter.Converter).union(
    {janus.converter.converter.Converter}
)

CONVERTERS = {c.__name__: c for c in CONVERTER_TYPES}


def get_collections_config():
    if collections_config_file.exists():
        with open(collections_config_file, "r") as f:
            config = json.load(f)
    else:
        config = {}
    return config
