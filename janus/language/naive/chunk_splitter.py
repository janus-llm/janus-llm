from janus.language.block import CodeBlock
from janus.language.naive.registry import register_splitter
from janus.language.node import NodeType
from janus.language.splitter import Splitter


@register_splitter("chunk")
class ChunkSplitter(Splitter):
    """
    Splits into fixed chunk sizes without parsing
    """

    def _get_ast(self, code: str) -> CodeBlock:
        return CodeBlock(
            text=code,
            name="root",
            id="root",
            start_point=(0, 0),
            end_point=(code.count("\n"), 0),
            start_byte=0,
            end_byte=len(bytes(code, "utf-8")),
            node_type=NodeType("program"),
            children=[],
            language=self.language,
            tokens=self._count_tokens(code),
        )
