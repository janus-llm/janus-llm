from typing import Callable, Dict

from ..splitter import Splitter

CUSTOM_SPLITTERS: Dict[str, Callable[..., Splitter]] = dict()


def register_splitter(name: str):
    def callback(splitter):
        CUSTOM_SPLITTERS[name] = splitter
        return splitter

    return callback
