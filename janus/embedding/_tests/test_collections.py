import datetime
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
        self.collections.create(EmbeddingType.PSEUDO)

        metadata = {
            "date_updated": datetime.datetime.now().date().isoformat(),
            "time_updated": datetime.datetime.now().time().isoformat("minutes"),
        }

        self._db.create_collection.assert_called_with("pseudo_1", metadata=metadata)

    def test_creation_triangulation(self):
        self.collections.create(EmbeddingType.REQUIREMENT)

        metadata = {
            "date_updated": datetime.datetime.now().date().isoformat(),
            "time_updated": datetime.datetime.now().time().isoformat("minutes"),
        }

        self._db.create_collection.assert_called_with("requirement_1", metadata=metadata)

    def test_creation_of_existing_type(self):
        mock_collection = MagicMock()
        mock_collection.name.__eq__._mock_return_value = True
        self._db.list_collections.return_value = [mock_collection]

        self.collections.create(EmbeddingType.REQUIREMENT)
        metadata = {
            "date_updated": datetime.datetime.now().date().isoformat(),
            "time_updated": datetime.datetime.now().time().isoformat("minutes"),
        }
        self._db.create_collection.assert_called_with("requirement_2", metadata=metadata)

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
