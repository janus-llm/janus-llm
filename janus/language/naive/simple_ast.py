from ...utils.enums import LANGUAGES
from ..alc.alc import AlcListingSplitter, AlcSplitter
from ..mumps.mumps import MumpsSplitter
from ..treesitter import TreeSitterSplitter
from .registry import register_splitter


@register_splitter("ast-flex")
def get_flexible_ast(language: str, listing: bool, **kwargs):
    if language == "ibmhlasm":
        if listing:
            return AlcSplitter(**kwargs)
        else:
            return AlcListingSplitter(**kwargs)
    elif language == "mumps":
        return MumpsSplitter(**kwargs)
    else:
        return TreeSitterSplitter(language=language, **kwargs)


@register_splitter("ast-strict")
def get_strict_ast(language: str, listing: bool, **kwargs):
    kwargs.update(
        protected_node_types=LANGUAGES[language]["functional_node_types"],
        prune_unprotected=True,
    )
    if language == "ibmhlasm":
        if listing:
            return AlcSplitter(**kwargs)
        else:
            return AlcListingSplitter(**kwargs)
    elif language == "mumps":
        return MumpsSplitter(**kwargs)
    else:
        return TreeSitterSplitter(language=language, **kwargs)
