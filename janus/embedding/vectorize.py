import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence

from chromadb import API
from chromadb.api.models.Collection import Collection

from ..converter import Converter
from ..language.block import CodeBlock
from ..llm.models_info import TOKEN_LIMITS
from ..utils.enums import EmbeddingType
from .collections import Collections
from .database import ChromaEmbeddingDatabase


class Vectorizer(Converter):
    """Class for creating embeddings/vectors in a specified ChromaDB"""

    def __init__(
        self,
        client: API,
        source_language: str,
        max_tokens: None | int,
        model: None | str,
    ) -> None:
        """Initializes the Embedding class

        Arguments:
            client: ChromaDB client instance
            source_language: The source programming language.
            max_tokens: The maximum number of tokens to send to the embedding model at
                once. If `None`, the `Vectorizer` will use the default value for the
                `model`.
            model: The name of the model to use. This will also determine the `max_tokens`
                if that variable is not set.
        """
        if max_tokens is None:
            max_tokens = TOKEN_LIMITS[model]

        super().__init__(
            source_language=source_language,
            max_tokens=max_tokens,
        )
        self._db = client
        self._collections = Collections(self._db)

        super()._load_parameters()

    def create_collection(self, embedding_type: EmbeddingType) -> Collection:
        return self._collections.create(embedding_type)

    def collections(
        self, name: None | EmbeddingType | str = None
    ) -> Sequence[Collection]:
        return self._collections.get(name)

    def _add_nodes_recursively(
        self, code_block: CodeBlock, embedding_type: EmbeddingType, file_name: str
    ) -> None:
        """Embed all nodes in the tree rooted at `code_block`

        Arguments:
            code_block: CodeBlock to embed
            embedding_type: EmbeddingType to use
            file_name: Name of file containing `code_block`
        """
        nodes = [code_block]
        while nodes:
            node = nodes.pop(0)
            self._add(node, embedding_type, file_name)
            nodes.extend(node.children)

    def _add(
        self,
        code_block: CodeBlock,
        embedding_type: EmbeddingType,
        file_name: str  # perhaps this should be a relative path from the source, but for
        # now we're all in 1 directory
    ) -> bool:
        """Calculate `code_block` embedding, returning success & storing in `embedding_id`

        Arguments:
            code_block: CodeBlock to embed
            embedding_type: EmbeddingType to use
            file_name: Name of file containing `code_block`

        Returns:
            True if embedding was successful, False otherwise
        """
        if code_block.text:
            metadatas = [
                {
                    "type": code_block.type,
                    "original_filename": file_name,
                    "tokens": code_block.tokens,
                    "cost": 0,  # TranslatedCodeBlock has cost
                },
            ]
            # for now, dealing with missing metadata by skipping it
            if code_block.text is not None:
                metadatas[0]["hash"] = hash(code_block.text)
            if code_block.start_point is not None:
                metadatas[0]["start_line"] = code_block.start_point[0]
            if code_block.end_point is not None:
                metadatas[0]["end_line"] = code_block.end_point[0]
            the_text = [code_block.text]
            code_block.embedding_id = self.add_text(embedding_type, the_text, metadatas)[
                0
            ]
            return True
        return False

    def add_text(
        self,
        embedding_type: EmbeddingType,
        texts: list[str],
        metadatas: list[dict],
        ids: list[str] = None,
    ) -> list[str]:
        """Helper function that stores a single text (in an array) and associated
        metadatas, returning the embedding id

        Arguments:
            embedding_type: EmbeddingType to use
            texts: list of texts to store
            metadatas: list of metadatas to store
            ids: list of embedding ids (must match lengh of texts),
                 generated if not given by caller

        Returns:
            list of embedding ids. Raises ValueError if collection not found.
        """
        if ids is None:
            # logic from langchain add_texts
            ids = [str(uuid.uuid1()) for _ in texts]
        collections = self._collections.get(embedding_type)
        collections[0].add(ids=ids, documents=texts, metadatas=metadatas)
        return ids


class VectorizerFactory(ABC):
    """Interface for creating a Vectorizer independent of type of ChromaDB client"""

    @abstractmethod
    def create_vectorizer(
        self,
        source_language: str,
        max_tokens: None | int,
        model: None | str,
        path: str | Path,
    ) -> Vectorizer:
        """Factory method"""


class ChromaDBVectorizer(VectorizerFactory):
    """Factory for Vectorizer that uses ChromaEmbeddingDatabase"""

    def create_vectorizer(
        self,
        source_language: str = "fortran",
        max_tokens: None | int = None,
        model: None | str = "gpt4all",
        path: str | Path = Path.home() / ".janus" / "chroma" / "chroma-data",
    ) -> Vectorizer:
        """
        Arguments:
            source_language: The source programming language.
            max_tokens: The maximum number of tokens to send to the embedding model at
                once. If `None`, the `Vectorizer` will use the default value for the
                `model`.
            model: The name of the model to use. This will also determine the `max_tokens`
                if that variable is not set.
            path: The path to the ChromaDB. Can be either a string of a URL or path or a
                Path object

            Returns:
                Vectorizer
        """
        database = ChromaEmbeddingDatabase(path)
        return Vectorizer(database, source_language, max_tokens, model)
