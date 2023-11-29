import tempfile
import unittest
from pathlib import Path

from ...utils.enums import EmbeddingType
from ..vectorize import Vectorizer


class TestVectorize(unittest.TestCase):
    def setUp(self):
        self.vectorizer = Vectorizer(path=tempfile.gettempdir() + "/janus/test-vectorize")
        self.vectorizer._db.reset()
        self.test_file = Path("janus/language/treesitter/_tests/languages/fortran.f90")
        self.test_block = self.vectorizer._splitter.split(self.test_file)

    def test_collections(self):
        embedding_type = EmbeddingType.REQUIREMENT
        collections = self.vectorizer.collections()
        self.assertEqual(len(collections), 0)
        self.vectorizer.create_collection(embedding_type)
        collections = self.vectorizer.collections()
        self.assertEqual(len(collections), 1)
        collection = self.vectorizer.collections(embedding_type.name.lower())
        self.assertIsNotNone(collection)

    def test_add_nodes_recursively(self):
        embedding_type = EmbeddingType.SOURCE
        self.vectorizer.create_collection(embedding_type)
        self.vectorizer._add_nodes_recursively(
            self.test_block, embedding_type, self.test_file.name
        )
        # assert something here
