from janus.language.block import CodeBlock
from janus.language.naive.registry import register_splitter
from janus.language.node import NodeType
from janus.language.splitter import Splitter


@register_splitter("tag")
class TagSplitter(Splitter):
    """
    Splits code by tags inserted into code
    """

    def __init__(self, tag: str, *args, **kwargs):
        kwargs.update(protected_node_types=("chunk",))
        super().__init__(*args, **kwargs)
        self._tag = f"\n{tag}\n"

    def _get_ast(self, code: str) -> CodeBlock:
        chunks = code.split(self._tag)
        children = []
        start_line = 0
        start_byte = 0
        for i, chunk in enumerate(chunks):
            prefix = suffix = self._tag
            if i == 0:
                prefix = ""
            if i == len(chunks) - 1:
                suffix = ""
            end_byte = start_byte + len(bytes(chunk, "utf-8"))
            end_line = start_line + chunk.count("\n")
            end_char = len(chunk) - chunk.rfind("\n") - 1
            node = CodeBlock(
                text=chunk,
                name=f"Chunk {i}",
                id=f"Chunk {i}",
                start_point=(start_line, 0),
                end_point=(end_line, end_char),
                start_byte=start_byte,
                end_byte=end_byte,
                affixes=(prefix, suffix),
                node_type=NodeType("chunk"),
                children=[],
                language=self.language,
                tokens=self._count_tokens(chunk),
            )
            children.append(node)
            start_line = end_line
            start_byte = end_byte
        return CodeBlock(
            text=code,
            name="root",
            id="root",
            start_point=(0, 0),
            end_point=(code.count("\n"), 0),
            start_byte=0,
            end_byte=len(bytes(code, "utf-8")),
            node_type=NodeType("program"),
            children=children,
            language=self.language,
            tokens=self._count_tokens(code),
        )
