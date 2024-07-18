from ..block import CodeBlock
from ..naive.chunk_splitter import ChunkSplitter
from ..naive.registry import register_splitter
from ..splitter import FileSizeError


@register_splitter("file")
class FileSplitter(ChunkSplitter):
    """
    Splits based on the entire file of the code
    """

    def _split_into_lines(self, node: CodeBlock):
        raise FileSizeError("File too large for basic splitter")
