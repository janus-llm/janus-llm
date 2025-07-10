import unittest
from pathlib import Path

from janus.language.naive.chunk_splitter import ChunkSplitter
from janus.retrievers.alc_retriever import OpCodeRetriever


class TestOpCodeRetriever(unittest.TestCase):
    def setUp(self):
        self._retriever = OpCodeRetriever("janus/retrievers/_tests/op_codes.json")

    def test_retrieval(self):
        test_file = Path("janus/language/treesitter/_tests/languages/ibmhlasm.asm")
        with open(test_file, "r") as f:
            text = f.read()
        splitter = ChunkSplitter(language="ibmhlasm")
        block = splitter.split_string(text, "test")
        context = self._retriever.get_context(block)
        self.assertEqual(context, "DS: Define Storage\n")
