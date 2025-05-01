import json
from pathlib import Path
from typing import Type

from janus.converter.converter import Converter
from janus.refiners.refiner import JanusRefiner

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


REFINER_TYPES = get_subclasses(JanusRefiner).union({JanusRefiner})
REFINERS = {r.__name__: r for r in REFINER_TYPES}

CONVERTER_TYPES = get_subclasses(Converter).union({Converter})

CONVERTERS: dict[str, Type[Converter]] = {c.__name__: c for c in CONVERTER_TYPES}


def get_collections_config():
    if collections_config_file.exists():
        with open(collections_config_file, "r") as f:
            config = json.load(f)
    else:
        config = {}
    return config


def key_value_arg(value: str) -> tuple[str, str | int | float]:
    try:
        key, val = value.split("=", 1)
    except ValueError:
        raise ValueError(f"{value!r} is not a valid key=value pair")

    try:
        val = float(val)
    except ValueError:
        pass
    else:
        if int(val) == val:
            val = int(val)

    return key, val
