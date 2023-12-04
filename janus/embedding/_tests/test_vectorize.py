import tempfile
import unittest
from pathlib import Path

from ...utils.enums import EmbeddingType
from ..vectorize import Vectorizer


class TestVectorize(unittest.TestCase):
    def setUp(self):
        self.vectorizer = Vectorizer(path=tempfile.gettempdir() + "/janus/test-vectorize")
        self.test_file = Path("janus/language/treesitter/_tests/languages/fortran.f90")
        self.test_block = self.vectorizer._splitter.split(self.test_file)

    def tearDown(self):
        self.vectorizer._db.reset()

    def test_add_nodes_recursively(self):
        embedding_type = EmbeddingType.SOURCE
        self.vectorizer.create_collection(embedding_type)
        self.vectorizer._add_nodes_recursively(
            self.test_block, embedding_type, self.test_file.name
        )
        # assert something here
