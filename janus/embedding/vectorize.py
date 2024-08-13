import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from chromadb import Client, Collection
from langchain_community.vectorstores import Chroma

from janus.embedding.collections import Collections
from janus.embedding.database import ChromaEmbeddingDatabase
from janus.language.block import CodeBlock, TranslatedCodeBlock
from janus.utils.enums import EmbeddingType


class Vectorizer(object):
    """Class for creating embeddings/vectors in a specified ChromaDB"""

    def __init__(self, client: Client, config: Optional[Dict[str, Any]] = None) -> None:
        """Initializes the Vectorizer class

        Arguments:
            client: ChromaDB client instance
        """
        self._db = client
        self._collections = Collections(self._db, config)

    def get_or_create_collection(
        self, name: EmbeddingType | str, model_name: Optional[str] = None
    ) -> Chroma:
        return self._collections.get_or_create(name, model_name=model_name)

    def create_collection(
        self, embedding_type: EmbeddingType, model_name: Optional[str] = None
    ) -> Chroma:
        return self._collections.create(embedding_type, model_name=model_name)

    def collections(
        self, name: None | EmbeddingType | str = None
    ) -> Sequence[Collection]:
        return self._collections.get(name)

    def add_nodes_recursively(
        self, code_block: CodeBlock, collection_name: EmbeddingType | str, file_name: str
    ) -> None:
        """Embed all nodes in the tree rooted at `code_block`

        Arguments:
            code_block: CodeBlock to embed
            collection_name: Collection to add to
            file_name: Name of file containing `code_block`
        """
        nodes = [code_block]
        while nodes:
            node = nodes.pop(0)
            self._add(node, collection_name, file_name)
            nodes.extend(node.children)

    def _add(
        self,
        code_block: CodeBlock,
        collection_name: EmbeddingType | str,
        filename: str,  # perhaps this should be a relative path from the source, but for
        # now we're all in 1 directory
    ) -> None:
        """Calculate `code_block` embedding, returning success & storing in `embedding_id`

        Arguments:
            code_block: CodeBlock to embed
            collection_name: Collection to add to
            filename: Name of file containing `code_block`
        """
        if code_block.text:
            metadatas = [
                {
                    "type": code_block.node_type,
                    "id": code_block.id,
                    "name": code_block.name,
                    "language": code_block.language,
                    "filename": filename,
                    "tokens": code_block.tokens,
                    "cost": 0,  # TranslatedCodeBlock has cost
                },
            ]
            if collection_name in self.config:
                metadatas[0]["embedding_model"] = self.config[collection_name]
            # for now, dealing with missing metadata by skipping it
            if isinstance(code_block, TranslatedCodeBlock):
                self._add(
                    code_block=code_block.original,
                    collection_name=collection_name,
                    filename=filename,
                )
                if code_block.original.embedding_id is not None:
                    metadatas[0][
                        "original_embedding_id"
                    ] = code_block.original.embedding_id
                metadatas[0]["cost"] = code_block.cost
            if code_block.text is not None:
                metadatas[0]["hash"] = hash(code_block.text)
            if code_block.start_point is not None:
                metadatas[0]["start_line"] = code_block.start_point[0]
            if code_block.end_point is not None:
                metadatas[0]["end_line"] = code_block.end_point[0]
            # TODO: Add metadata about translation parameters (e.g. model)
            the_text = [code_block.text]
            code_block.embedding_id = self.add_text(
                collection_name,
                the_text,
                metadatas,
            )[0]

    def add_text(
        self,
        collection_name: EmbeddingType | str,
        texts: list[str],
        metadatas: list[dict],
        ids: list[str] = None,
    ) -> list[str]:
        """Helper function that stores a single text (in an array) and associated
        metadatas, returning the embedding id

        Arguments:
            collection_name: Collection to add to
            texts: list of texts to store
            metadatas: list of metadatas to store
            ids: list of embedding ids (must match lengh of texts),
                 generated if not given by caller

        Returns:
            list of embedding ids. Raises ValueError if collection not found.
        """
        if ids is None:
            # Logic originally from langchain's vectorstores.chroma.Chroma.add_texts
            # Modified to use uuid3 instead of uuid1. We don't need to update
            # an entry in the database if the text is the same. So we generate the UUID
            # based on the text.
            ids = [str(uuid.uuid3(uuid.NAMESPACE_DNS, text)) for text in texts]
        collection = self._collections.get_or_create(collection_name)
        collection.add_texts(ids=ids, texts=texts, metadatas=metadatas)
        return ids

    @property
    def config(self):
        return self._collections._config


class VectorizerFactory(ABC):
    """Interface for creating a Vectorizer independent of type of ChromaDB client"""

    @abstractmethod
    def create_vectorizer(
        self, path: str | Path, config: Dict[str, Any] = {}
    ) -> Vectorizer:
        """Factory method"""


class ChromaDBVectorizer(VectorizerFactory):
    """Factory for Vectorizer that uses ChromaEmbeddingDatabase"""

    def create_vectorizer(
        self,
        path: str | Path = Path.home() / ".janus" / "chroma" / "chroma-data",
        config: Optional[Dict[str, Any]] = None,
    ) -> Vectorizer:
        """
        Arguments:
            path: The path to the ChromaDB. Can be either a string of a URL or path or a
                Path object

            Returns:
                Vectorizer
        """
        database = ChromaEmbeddingDatabase(path)
        return Vectorizer(database, config)
