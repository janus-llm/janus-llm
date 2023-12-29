import unittest
from unittest.mock import MagicMock

import pytest

from janus.embedding.collections import Collections
from janus.utils.enums import EmbeddingType


class TestCollections(unittest.TestCase):
    def setUp(self):
        self._db = MagicMock()
        self.collections = Collections(self._db)

    def test_creation(self):
        self._db.create_collection.return_value = "foo"

        result = self.collections.create(EmbeddingType.PSEUDO)

        self._db.create_collection.assert_called_with("pseudo")
        self.assertEqual(result, "foo")

    def test_creation_triangulation(self):
        self._db.create_collection.return_value = []

        result = self.collections.create(EmbeddingType.REQUIREMENT)

        self._db.create_collection.assert_called_with("requirement")
        self.assertEqual(result, [])

    def test_creation_of_existing_type(self):
        mock_collection = MagicMock()
        mock_collection.name.__eq__._mock_return_value = True
        self._db.list_collections.return_value = [mock_collection]

        self.collections.create(EmbeddingType.REQUIREMENT)

        self._db.create_collection.assert_called_with("requirement_2")

    def test_missing_embedding_type(self):
        with pytest.raises(ValueError):
            self.collections.create(EmbeddingType(1337))

    def test_get_with_None_name(self):
        self._db.list_collections.return_value = 1337

        result = self.collections.get()

        self.assertTrue(self._db.list_collections.called)
        self.assertEqual(result, 1337)
        self.assertFalse(self._db.get_collection.called)

    def test_get_with_embedding_type(self):
        self._db.get_collection.return_value = "blah"

        result = self.collections.get(EmbeddingType.SOURCE)

        self._db.get_collection.assert_called_once_with("source")
        self.assertEqual(result, ["blah"])
        self.assertFalse(self._db.list_collections.called)

    def test_get_with_string_name(self):
        self._db.get_collection.return_value = "xxx"

        result = self.collections.get("foo")

        self._db.get_collection.assert_called_with("foo")
        self.assertEqual(result, ["xxx"])
        self.assertFalse(self._db.list_collections.called)