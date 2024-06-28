from janus.language.block import CodeBlock
from janus.language.naive.chunk_splitter import ChunkSplitter
from janus.language.naive.registry import register_splitter
from janus.language.splitter import FileSizeError


@register_splitter("file")
class FileSplitter(ChunkSplitter):
    """
    Splits based on the entire file of the code
    """

    def _split_into_lines(self, node: CodeBlock):
        raise FileSizeError("File too large for basic splitter")
