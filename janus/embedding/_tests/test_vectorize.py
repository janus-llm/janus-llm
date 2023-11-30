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
        self.assertEqual(len(collections), 0, "precondition failed")

        orig_collection = self.vectorizer.create_collection(embedding_type)
        collections = self.vectorizer.collections()
        self.assertEqual(len(collections), 1, "failed to add collection")
        self.assertEqual(orig_collection, collections[0], "didn't find added collection")

        retrieved_collections = self.vectorizer.collections(embedding_type)
        self.assertEqual(len(retrieved_collections), 1, "couldn't find by type")
        self.assertEqual(
            orig_collection,
            retrieved_collections[0],
            "didn't find correct collection by type",
        )

        retrieved_collections = self.vectorizer.collections(embedding_type.name.lower())
        self.assertEqual(len(retrieved_collections), 1, "couldn't find by name")
        self.assertEqual(
            orig_collection,
            retrieved_collections[0],
            "didn't find correct collection by name",
        )

        duplicate_type_collection = self.vectorizer.create_collection(embedding_type)
        collections = self.vectorizer.collections()
        self.assertEqual(len(collections), 2, "second collection not added")
        self.assertNotEquals(
            orig_collection,
            duplicate_type_collection,
            "second collection should be separate from original",
        )
        self.assertEqual(
            "requirement_2",
            duplicate_type_collection.name,
            "expected collection name to increment base type",
        )

    def test_add_nodes_recursively(self):
        embedding_type = EmbeddingType.SOURCE
        self.vectorizer.create_collection(embedding_type)
        self.vectorizer._add_nodes_recursively(
            self.test_block, embedding_type, self.test_file.name
        )
        # assert something here
