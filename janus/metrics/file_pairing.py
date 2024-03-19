from typing import Any, Callable, Dict, List, Optional, Tuple

from janus.language.binary import BinarySplitter
from janus.language.mumps import MumpsSplitter
from janus.language.node import NodeType
from janus.language.treesitter import TreeSitterSplitter
from janus.utils.enums import CUSTOM_SPLITTERS

FILE_PAIRING_METHODS: Dict[str, Callable[[str, str], List[Tuple[str, str]]]] = {}


def register_pairing_method(name: Optional[str] = None):
    """
    Registers a pairing method for pairing strings between files
    """

    def decorator(f: Callable[[str, str], List[Tuple[str, str]]]):
        if name is None:
            pairing_name = f.__name__
        else:
            pairing_name = name
        FILE_PAIRING_METHODS[pairing_name] = f
        return f

    return decorator


@register_pairing_method()
def PAIR_BY_FILE(src: str, cmp: str, state: Dict[str, Any]) -> List[Tuple[str, str]]:
    """
    Pairs the entire contents of a file together
    :param src src file text
    :param cmp cmp file text
    :param state current evaluation state
    """
    return [(src, cmp)]


@register_pairing_method()
def PAIR_BY_LINE(src: str, cmp: str, state: Dict[str, Any]) -> List[Tuple[str, str]]:
    """
    Pairs the contents of a file together by line
    :param src src file text
    :param cmp cmp file text
    :param state current evaluation state
    """
    return list(zip(src.split("\n"), cmp.split("\n")))


@register_pairing_method()
def PAIR_BY_LINE_COMMENT(
    src: str, cmp: str, state: Dict[str, Any]
) -> List[Tuple[str, str]]:
    """
    Pairs the comments of a file together by line
    :param src src file text
    :param cmp cmp file text
    :param state current evaluation state
    """
    kwargs = dict(
        max_tokens=state["token_limit"] // 2.5,
        model=state["llm"],
        protected_node_types=(NodeType("comment"),),
        prune_node_types=tuple(),
    )
    if state["lang"] in CUSTOM_SPLITTERS:
        if state["lang"] == "mumps":
            splitter = MumpsSplitter(**kwargs)
        elif state["lang"] == "binary":
            splitter = BinarySplitter(**kwargs)
    else:
        splitter = TreeSitterSplitter(language=state["lang"], **kwargs)
    src_tree = splitter.split(state["src_file"], prune_unprotected=False)
    cmp_tree = splitter.split(state["cmp_file"])
    pairs = []

    def _parse_pairs(node1, node2, pairs):
        for c1, c2 in zip(node1.children, node2.children):
            if c1.node_type == "comment" and c2.node_type == "comment":
                pairs.append((c1.complete_text, c2.complete_text))
            else:
                _parse_pairs(c1, c2, pairs)

    _parse_pairs(src_tree, cmp_tree, pairs)
    return pairs
