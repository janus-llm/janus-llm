import uuid
from pathlib import Path

from chromadb.api.models.Collection import Collection

from ..converter import Converter
from ..language.block import CodeBlock
from ..llm.models_info import TOKEN_LIMITS
from ..utils.enums import EmbeddingType
from .database import ChromaEmbeddingDatabase
from .embeddings import get_embeddings


class Vectorizer(Converter):
    """Class for creating embeddings/vectors in a specified ChromaDB"""

    def __init__(
        self,
        source_language: str = "fortran",
        max_tokens: None | int = None,
        model: None | str = "gpt4all",
        path: str | Path = Path.home() / ".janus" / "chroma" / "chroma-data",
    ) -> None:
        """Initializes the Embedding class

        Arguments:
            source_language: The source programming language.
            max_tokens: The maximum number of tokens to send to the embedding model at
                once. If `None`, the `Vectorizer` will use the default value for the
                `model`.
            model: The name of the model to use. This will also determine the `max_tokens`
                if that variable is not set.
            path: The path to the ChromaDB. Can be either a string of a URL or path or a
                Path object
        """
        if max_tokens is None:
            max_tokens = TOKEN_LIMITS[model]

        super().__init__(
            source_language=source_language,
            max_tokens=max_tokens,
        )
        self._embeddings = get_embeddings(model)
        self._db = ChromaEmbeddingDatabase(path)

        super()._load_parameters()

    def create_collection(self, embedding_type: EmbeddingType) -> None:
        """Create a Chroma collection for the given embedding type.

        Arguments:
            embedding_type: The type of embedding to create the vector store for
        """
        # First, check if the embedding type exists
        if embedding_type not in EmbeddingType:
            raise ValueError(f"Invalid embedding type: {embedding_type}")
        # Now check if the collection exists
        if embedding_type in self.collections():
            # If it does, create a new collection with a similar but incremented name
            # ex. "requirement" -> "requirement_1"
            # Count the number of collections with the same embedding type
            type_collections = [
                collection
                for collection in self.collections()
                if collection.startswith(embedding_type.name.lower())
            ]
            # TODO: do we want to iterate over similarly named collections?
            collection_name = f"{embedding_type.name.lower()}_{len(type_collections) + 1}"
        else:
            collection_name = embedding_type.name.lower()
        self._db.create_collection(collection_name)

    def collections(self, name: None | EmbeddingType | str = None) -> list[Collection]:
        """Get the Chroma collections for this vectorizer.

        Returns:
            The Chroma collections for this vectorizer
        """
        if isinstance(name, str):
            try:
                return self._db.get_collection(name)
            except ValueError:
                return []
        elif isinstance(name, EmbeddingType):
            return [self._db.get_collection(name.name.lower())]
        else:
            return self._db.list_collections()

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
            code_block.embedding_id = self._add_text_to_vector_store(
                embedding_type, the_text, metadatas
            )[0]
            return True
        return False

    def _add_text_to_vector_store(
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
            list of embedding ids
        """
        if ids is None:
            # logic from langchain add_texts
            ids = [str(uuid.uuid1()) for _ in texts]
        collections = self.collections(embedding_type)
        collections[0].add(ids=ids, documents=texts, metadatas=metadatas)
        return ids
