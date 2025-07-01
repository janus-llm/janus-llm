import unittest
from pathlib import Path

from janus.language.naive.chunk_splitter import ChunkSplitter
from janus.retrievers.alc_retriever import OpCodeRetriever


class TestOpCodeRetriever(unittest.TestCase):
    def setUp(self):
        # TODO: add alc op code retriever
        self._retriever = OpCodeRetriever("janus/retrievers/_tests/op_codes.json")

    def test_retrieval(self):
        # TODO: Check result
        test_file = Path("janus/language/treesitter/_tests/languages/ibmhlasm.asm")
        with open(test_file, "r") as f:
            text = f.read()
        splitter = ChunkSplitter()
        block = splitter.split_string(text)
        context = self._retriever.get_context(block)
        self.assertEqual(context, "DS: Define Storage")
