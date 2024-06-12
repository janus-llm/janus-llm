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
        current_string = lines[0]
        num_chunks = 0
        start_line = 0
        end_line = 1
        start_byte = 0
        for line in lines[1:]:
            num_tokens = self._count_tokens(current_string + "\n" + line)
            if num_tokens < self._chunk_size:
                current_string += "\n" + line
                end_line += 1
            else:
                end_byte = start_byte + len(bytes(current_string, "utf-8"))
                end_char = len(current_string) - current_string.rfind("\n") - 1
                prefix = "\n".join(lines[:start_line])
                suffix = "\n".join(lines[end_line:])
                node = CodeBlock(
                    text=current_string,
                    name=f"chunk {num_chunks+1}",
                    id=f"chunk {num_chunks+1}",
                    start_point=(start_line, 0),
                    end_point=(end_line, end_char),
                    start_byte=start_byte,
                    end_byte=end_byte,
                    affixes=(prefix, suffix),
                    node_type=NodeType("chunk"),
                    children=[],
                    language=self.language,
                    tokens=self._count_tokens(current_string),
                )
                children.append(node)
                # TODO: create new node to children
                current_string = line
                num_chunks += 1
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
