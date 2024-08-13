from typing import Any, Callable

from janus.language.binary import BinarySplitter
from janus.language.mumps import MumpsSplitter
from janus.language.node import NodeType
from janus.language.treesitter import TreeSitterSplitter
from janus.utils.enums import CUSTOM_SPLITTERS

FILE_PAIRING_METHODS: dict[str, Callable[[str, str], list[tuple[str, str]]]] = {}


def register_pairing_method(name: None | str = None) -> Callable[[Callable], Callable]:
    """Registers a pairing method for pairing strings between files

    Arguments:
        name: The name of the pairing method. If None, the function name is used.
        help: The help text for the pairing method.

    Returns:
        The decorator function.
    """

    def decorator(f: Callable[[str, str], list[tuple[str, str]]]):
        if name is None:
            pairing_name = f.__name__
        else:
            pairing_name = name
        FILE_PAIRING_METHODS[pairing_name] = f
        return f

    return decorator


@register_pairing_method(name="file")
def pair_by_file(
    target: str, reference: str, **kwargs: dict[str, Any]
) -> list[tuple[str, str]]:
    """Pairs the entire contents of a file together

    Arguments:
        target: The target file text.
        reference: The reference file text.
        state: The current evaluation state.

    Returns:
        A list of tuples of the target and reference file text.
    """
    return [(target, reference)]


@register_pairing_method(name="line")
def pair_by_line(
    target: str, reference: str, **kwargs: dict[str, Any]
) -> list[tuple[str, str]]:
    """Pairs the contents of a file together by line

    Arguments:
        target: The target file text.
        reference: The reference file text.
        state: The current evaluation state.

    Returns:
        A list of tuples of the target and reference file text.
    """
    return list(zip(target.split("\n"), reference.split("\n")))


@register_pairing_method(name="line-comment")
def pair_by_line_comment(
    target: str, reference: str, **kwargs: dict[str, Any]
) -> list[tuple[str, str]]:
    """Pairs the comments of a file together by line

    **WARNING**: Do not use, as this method is extremely brittle.

    Arguments:
        target: The target file text.
        reference: The reference/reference file text.
        state: The current evaluation state.

    Returns:
        A list of tuples of the target and reference file text.
    """
    splitter_kwargs = dict(
        max_tokens=kwargs["token_limit"] // 2.5,
        model=kwargs["llm"],
        protected_node_types=(NodeType("comment"),),
        prune_node_types=tuple(),
    )
    if kwargs["target_file"] is None or kwargs["reference_file"] is None:
        raise ValueError("Error: must provide file for pair by line comment")
    if kwargs["lang"] is None:
        raise ValueError("Error: must provide language for pair by line comment")
    if kwargs["lang"] in CUSTOM_SPLITTERS:
        if kwargs["lang"] == "mumps":
            splitter = MumpsSplitter(**splitter_kwargs)
        elif kwargs["lang"] == "binary":
            splitter = BinarySplitter(**splitter_kwargs)
    else:
        splitter = TreeSitterSplitter(language=kwargs["lang"], **splitter_kwargs)
    target_tree = splitter.split(kwargs["target_file"])
    reference_tree = splitter.split(kwargs["reference_file"])
    pairs = []

    def _parse_pairs(node1, node2, pairs):
        for c1, c2 in zip(node1.children, node2.children):
            if c1.node_type == "comment" and c2.node_type == "comment":
                pairs.append((c1.complete_text, c2.complete_text))
            else:
                _parse_pairs(c1, c2, pairs)

    _parse_pairs(target_tree, reference_tree, pairs)
    return pairs
