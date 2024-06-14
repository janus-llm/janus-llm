from janus.language.block import CodeBlock
from janus.language.naive.chunk_splitter import ChunkSplitter
from janus.language.naive.registry import register_splitter


@register_splitter("file_splitter")
class FileSplitter(ChunkSplitter):
    """
    Splits based on the entire file of the code
    """

    def _split_into_lines(self, node: CodeBlock):
        raise ValueError("Error: File to large for basic splitter")
