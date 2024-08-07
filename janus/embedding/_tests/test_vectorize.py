import datetime
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from chromadb.api.client import Client

from janus.embedding.vectorize import Vectorizer, VectorizerFactory
from janus.language.treesitter import TreeSitterSplitter
from janus.utils.enums import EmbeddingType


class MockDBVectorizer(VectorizerFactory):
    """Factory for Vectorizer that uses ChromaEmbeddingDatabase"""

    def __init__(self, database: Client):
        self._db = database

    def create_vectorizer(
        self,
        source_language: str = "fortran",
        max_tokens: None | int = None,
        model: None | str = "gpt4all",
        path: str | Path = None,
    ) -> Vectorizer:
        return Vectorizer(self._db)


class TestVectorize(unittest.TestCase):
    def setUp(self):
        self.database = MagicMock(Client)

        def list_collections():
            return []

        self.database.list_collections = list_collections
        self.vectorizer = MockDBVectorizer(self.database).create_vectorizer()
        self.test_file = Path("janus/language/treesitter/_tests/languages/fortran.f90")
        splitter = TreeSitterSplitter(
            language="fortran",
            max_tokens=16_384,
        )
        self.test_block = splitter.split(self.test_file)

    def test_add_nodes_recursively(self):
        embedding_type = EmbeddingType.SOURCE
        self.vectorizer.create_collection(embedding_type)
        metadata = {
            "date_updated": datetime.datetime.now().date().isoformat(),
            "time_updated": datetime.datetime.now().time().isoformat("minutes"),
        }
        self.database.create_collection.assert_called_with("source_1", metadata=metadata)
        self.vectorizer.add_nodes_recursively(
            self.test_block, embedding_type, self.test_file.name
        )
        self.database.get_or_create_collection.assert_called_with(
            name="source_1", embedding_function=None, metadata=metadata
        )
