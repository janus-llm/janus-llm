from janus.language.alc.alc import AlcSplitter
from janus.language.mumps.mumps import MumpsSplitter
from janus.language.naive.registry import register_splitter
from janus.language.treesitter import TreeSitterSplitter
from janus.utils.enums import LANGUAGES


@register_splitter("ast-flex")
def get_flexible_ast(language: str, **kwargs):
    if language == "ibmhlasm":
        return AlcSplitter(**kwargs)
    elif language == "mumps":
        return MumpsSplitter(**kwargs)
    else:
        return TreeSitterSplitter(language=language, **kwargs)


@register_splitter("ast-strict")
def get_strict_ast(language: str, **kwargs):
    kwargs.update(
        protected_node_types=LANGUAGES[language]["functional_node_types"],
        prune_unprotected=True,
    )
    if language == "ibmhlasm":
        return AlcSplitter(**kwargs)
    elif language == "mumps":
        return MumpsSplitter(**kwargs)
    else:
        return TreeSitterSplitter(language=language, **kwargs)
