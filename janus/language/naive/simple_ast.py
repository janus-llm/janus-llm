from janus.language.naive.registry import register_splitter
from janus.language.treesitter import TreeSitterSplitter
from janus.utils.enums import LANGUAGES


@register_splitter("ast-flex")
class FlexibleTreeSitterSplitter(TreeSitterSplitter):
    pass


@register_splitter("ast-strict")
class StrictTreeSitterSplitter(TreeSitterSplitter):
    def __init__(self, language: str, **kwargs):
        kwargs.update(
            protected_node_types=(LANGUAGES[language]["functional_node_type"],),
            prune_unprotected=True,
        )
        super().__init__(language=language, **kwargs)
