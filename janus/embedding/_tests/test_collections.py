import tempfile
import unittest

from janus.embedding.collections import Collections
from janus.embedding.database import ChromaEmbeddingDatabase
from janus.utils.enums import EmbeddingType


class TestCollections(unittest.TestCase):
    def setUp(self):
        # temporarily use file system
        path = tempfile.gettempdir() + "/janus/test-vectorize"
        self._db = ChromaEmbeddingDatabase(path)
        self.collections = Collections(self._db)

    def tearDown(self):
        self._db.reset()

    def test_collections(self):
        embedding_type = EmbeddingType.REQUIREMENT
        collections = self.collections.get()
        self.assertEqual(len(collections), 0, "precondition failed")

        orig_collection = self.collections.create(embedding_type)
        collections = self.collections.get()
        self.assertEqual(len(collections), 1, "failed to add collection")
        self.assertEqual(orig_collection, collections[0], "didn't find added collection")

        retrieved_collections = self.collections.get(embedding_type)
        self.assertEqual(len(retrieved_collections), 1, "couldn't find by type")
        self.assertEqual(
            orig_collection,
            retrieved_collections[0],
            "didn't find correct collection by type",
        )

        retrieved_collections = self.collections.get(embedding_type.name.lower())
        self.assertEqual(len(retrieved_collections), 1, "couldn't find by name")
        self.assertEqual(
            orig_collection,
            retrieved_collections[0],
            "didn't find correct collection by name",
        )

        duplicate_type_collection = self.collections.create(embedding_type)
        collections = self.collections.get()
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

        self.assertRaises(ValueError, self.collections.get, "foo")
        self.assertRaises(ValueError, self.collections.get, EmbeddingType.SUMMARY)
