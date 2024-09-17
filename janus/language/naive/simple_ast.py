from janus.language.alc.alc import AlcListingSplitter, AlcSplitter
from janus.language.mumps.mumps import MumpsSplitter
from janus.language.naive.registry import register_splitter
from janus.language.splitter import Splitter
from janus.language.treesitter import TreeSitterSplitter
from janus.utils.enums import LANGUAGES
from janus.utils.logger import create_logger

log = create_logger(__name__)


@register_splitter("ast-flex")
def get_flexible_ast(language: str, **kwargs) -> Splitter:
    """Get a flexible AST splitter for the given language.

    Arguments:
        language: The language to get the splitter for.

    Returns:
        A flexible AST splitter for the given language.
    """
    kwargs.update(protected_node_types=())
    if language == "ibmhlasm":
        return AlcSplitter(**kwargs)
    elif language == "mumps":
        return MumpsSplitter(**kwargs)
    else:
        return TreeSitterSplitter(language=language, **kwargs)


@register_splitter("ast-strict")
def get_strict_ast(language: str, prune_unprotected=True, **kwargs) -> Splitter:
    """Get a strict AST splitter for the given language.

    The strict splitter will only return nodes that are of a functional type.

    Arguments:
        language: The language to get the splitter for.

    Returns:
        A strict AST splitter for the given language.
    """
    kwargs.update(
        protected_node_types=LANGUAGES[language]["functional_node_types"],
        prune_unprotected=prune_unprotected,
    )
    if language == "ibmhlasm":
        return AlcSplitter(**kwargs)
    elif language == "mumps":
        return MumpsSplitter(**kwargs)
    else:
        return TreeSitterSplitter(language=language, **kwargs)


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
    kwargs.update(
        protected_node_types=LANGUAGES[language]["functional_node_types"],
        prune_unprotected=True,
    )
    if language == "ibmhlasm":
        return AlcListingSplitter(**kwargs)
    else:
        log.warning("Listing splitter is only intended for use with IBMHLASM!")
        return TreeSitterSplitter(language=language, **kwargs)


@register_splitter("ast-flex-listing")
def get_flexible_listing_ast(language: str, **kwargs) -> Splitter:
    """Get a flexible AST splitter for the given language. This splitter is intended for
    use with IBM HLASM.

    Arguments:
        language: The language to get the splitter for.

    Returns:
        A flexible AST splitter for the given language.
    """
    if language == "ibmhlasm":
        return AlcListingSplitter(**kwargs)
    else:
        log.warning("Listing splitter is only intended for use with IBMHLASM!")
        return TreeSitterSplitter(language=language, **kwargs)
