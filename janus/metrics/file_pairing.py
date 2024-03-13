from typing import Callable, Dict, List, Optional, Tuple

FILE_PAIRING_METHODS: Dict[str, Callable[[str, str], List[Tuple[str, str]]]] = {}


def register_pairing_method(name: Optional[str] = None):
    def decorator(f: Callable[[str, str], List[Tuple[str, str]]]):
        if name is None:
            pairing_name = f.__name__
        else:
            pairing_name = name
        FILE_PAIRING_METHODS[pairing_name] = f
        return f

    return decorator


@register_pairing_method()
def PAIR_BY_FILE(src: str, cmp: str) -> List[Tuple[str, str]]:
    return [(src, cmp)]


@register_pairing_method()
def PAIR_BY_LINE(src: str, cmp: str) -> List[Tuple[str, str]]:
    return list(zip(src.split("\n"), cmp.split("\n")))
