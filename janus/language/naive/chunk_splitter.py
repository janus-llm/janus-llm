from janus.language.block import CodeBlock
from janus.language.splitter import Splitter

from ..node import NodeType


class ChunkSplitter(Splitter):
    def __init__(self, chunk_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._chunk_size = chunk_size

    def _get_ast(self, code: str) -> CodeBlock:
        lines = code.split("\n")
        children = []
        current_string = ""
        # num_chunks = 0
        # start_line = 0
        # start_char = 0
        for line in lines:
            num_tokens = self._count_tokens(current_string + "\n" + line)
            if num_tokens < self._chunk_size:
                current_string += "\n" + line
            else:
                # node = CodeBlock(
                #     text=current_string,
                #     name=f"chunk {num_chunks+1}",
                #     id=f"chunk {num_chunks+1}",
                # )
                # TODO: create new node to children
                current_string = line
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
