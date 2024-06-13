from janus.language.block import CodeBlock
from janus.language.naive.chunk_splitter import ChunkSplitter


class BasicSplitter(ChunkSplitter):
    def _split_into_lines(self, node: CodeBlock):
        raise ValueError("Error: File to large for basic splitter")
