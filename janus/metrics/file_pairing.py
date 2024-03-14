from typing import Any, Callable, Dict, List, Optional, Tuple

# from janus.language.binary import BinarySplitter
# from janus.language.mumps import MumpsSplitter
# from janus.language.treesitter import TreeSitterSplitter
# from janus.utils.enums import CUSTOM_SPLITTERS

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
def PAIR_BY_FILE(src: str, cmp: str, state: Dict[str, Any]) -> List[Tuple[str, str]]:
    return [(src, cmp)]


@register_pairing_method()
def PAIR_BY_LINE(src: str, cmp: str, state: Dict[str, Any]) -> List[Tuple[str, str]]:
    return list(zip(src.split("\n"), cmp.split("\n")))


# @register_pairing_method()
# def PAIR_BY_LINE_COMMENT(
#     src: str, cmp: str,
#     state: Dict[str, Any]
# ) -> List[Tuple[str, str]]:
#     kwargs = dict(
#         max_tokens=state["token_limit"] // 2.5,
#         model=state["llm"],
#         protected_node_types=tuple( ),
#         prune_node_types=tuple(),
#     )
#     if state["lang"] in CUSTOM_SPLITTERS:
#         if state["lang"] == "mumps":
#             splitter = MumpsSplitter(**kwargs)
#         elif state["lang"] == "binary":
#             splitter = BinarySplitter(**kwargs)
#     else:
#         splitter = TreeSitterSplitter(language=state["lang"], **kwargs)
#     src_tree = splitter.split(state["src_file"], prune_unprotected=False)
#     cmp_tree = splitter.split(state["cmp_file"])
#     def _print_tree(node, prefix):
#         #print(prefix, node.node_type, node.complete_text)
#         print(prefix, node.node_type)
#         for c in node.children:
#             _print_tree(c, prefix+"\t")
#     _print_tree(src_tree, "")
#     return [(src, cmp)]
