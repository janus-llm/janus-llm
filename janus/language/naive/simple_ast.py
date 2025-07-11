from janus.language.alc.alc import AlcListingSplitter, AlcRegexSplitter, AlcSplitter
from janus.language.mumps.mumps import MumpsSplitter
from janus.language.naive.registry import register_splitter
from janus.language.splitter import Splitter
from janus.language.treesitter import TreeSitterSplitter
from janus.utils.enums import LANGUAGES
from janus.utils.logger import create_logger

log = create_logger(__name__)


def get_splitter(language: str, listing: bool = False, **kwargs) -> Splitter:
    if listing:
        if not language.startswith("ibmhlasm"):
            raise ValueError(
                'Listing splitter is only intended for use with ALC ("ibmhlasm"),'
                f' not "{language}"'
            )
        return AlcListingSplitter(**kwargs)

    if language == "ibmhlasm":
        return AlcRegexSplitter(**kwargs)
    if language == "ibmhlasm-ts":
        return AlcSplitter(**kwargs)

    if language == "mumps":
        return MumpsSplitter(**kwargs)

    return TreeSitterSplitter(language=language, **kwargs)


@register_splitter("ast-flex")
def get_flexible_ast(language: str, **kwargs) -> Splitter:
    """Get a flexible AST splitter for the given language.

    Arguments:
        language: The language to get the splitter for.

    Returns:
        A flexible AST splitter for the given language.
    """
    kwargs.update(protected_node_types=())
    return get_splitter(language=language, **kwargs)


@register_splitter("ast-strict")
def get_strict_ast(language: str, prune_unprotected=True, **kwargs) -> Splitter:
    """Get a strict AST splitter for the given language.

    The strict splitter will only return nodes that are of a functional type.

    Arguments:
        language: The language to get the splitter for.

    Returns:
        A strict AST splitter for the given language.
    """
    if "functional_node_types" not in LANGUAGES[language]:
        raise ValueError(
            f'Functional node not defined for {language}. Add a "functional_node_types"'
            f' key for "{language}" in `janus.utils.enums.LANGUAGES`'
        )
    kwargs.update(
        protected_node_types=LANGUAGES[language]["functional_node_types"],
        prune_unprotected=prune_unprotected,
    )
    return get_splitter(language=language, **kwargs)


@register_splitter("ast-data")
def get_data_ast(language: str, prune_unprotected=True, **kwargs) -> Splitter:
    """Get a data AST splitter for the given language.

    The data splitter will only return nodes that are of a data type.

    Arguments:
        language: The language to get the splitter for.

    Returns:
        A data AST splitter for the given language.
    """
    if "data_node_types" not in LANGUAGES[language]:
        raise ValueError(
            f'Data node not defined for {language}. Add a "data_node_types"'
            f' key for "{language}" in `janus.utils.enums.LANGUAGES`'
        )
    kwargs.update(
        protected_node_types=LANGUAGES[language]["data_node_types"],
        prune_unprotected=prune_unprotected,
    )
    return get_splitter(language=language, **kwargs)


@register_splitter("ast-strict-listing")
def get_strict_listing_ast(language: str, **kwargs) -> Splitter:
    """Get a strict AST splitter for the given language. This splitter is intended for
    use with IBM HLASM.

    The strict splitter will only return nodes that are of a functional type.

    Arguments:
        language: The language to get the splitter for.

    Returns:
        A strict AST splitter for the given language.
    """
    return get_strict_ast(language=language, listing=True, **kwargs)


@register_splitter("ast-flex-listing")
def get_flexible_listing_ast(language: str, **kwargs) -> Splitter:
    """Get a flexible AST splitter for the given language. This splitter is intended for
    use with IBM HLASM.

    Arguments:
        language: The language to get the splitter for.

    Returns:
        A flexible AST splitter for the given language.
    """
    return get_flexible_ast(language=language, listing=True, **kwargs)
