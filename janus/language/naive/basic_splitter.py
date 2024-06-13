from janus.language.block import CodeBlock

from .chunk_splitter import ChunkSplitter


class BasicSplitter(ChunkSplitter):
    def _split_into_lines(self, node: CodeBlock):
        raise ValueError("Error: File to large for basic splitter")
