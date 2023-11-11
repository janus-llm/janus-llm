from pathlib import Path

from langchain.schema.vectorstore import VectorStore

from ..converter import Converter
from ..language.block import CodeBlock
from ..utils.enums import EmbeddingType


class Vectorizer(Converter):
    """Class for creating embeddings/vectors in a specified ChromaDB"""

    def __init__(
        self,
        source_language: str = "fortran",
        parser_type: None | str = None,
        path: str | Path = Path.home() / ".janus" / "chroma" / "chroma-data",
    ) -> None:
        """Initializes the Embedding class

        Arguments:
            path: The path to the ChromaDB. Can be either a string of a URL or path or a
                Path object
        """
        super().__init__(source_language=source_language, parser_type=parser_type)
        # TODO: create a client for the DB based on the path
        # Check whether or not it's a URL. If it is, parse it and configure the settings
        # accordingly
        # self._db = chromadb.ChromaDB(path)

    def embeddings(self, embedding_type: EmbeddingType) -> VectorStore:
        """Get the Chroma vector store for the given embedding type.

        Arguments:
            embedding_type: The type of embedding to get the vector store for

        Returns:
            The Chroma vector store for the given embedding type
        """
        return self._collections[embedding_type]

    def _embed_nodes_recursively(
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
            self._embed(node, embedding_type, file_name)
            nodes.extend(node.children)

    def _embed(
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
            )
            return True
        return False

    def _add_text_to_vector_store(
        self, embedding_type: EmbeddingType, texts: list[str], metadatas: list[dict]
    ) -> list[str]:
        """Helper function that stores a single text (in an array) and associated
        metadatas, returning the embedding id

        Arguments:
            embedding_type: EmbeddingType to use
            texts: list of texts to store
            metadatas: list of metadatas to store

        Returns:
            list of embedding ids
        """
        vector_store = self.embeddings(embedding_type)
        return vector_store.add_texts(texts, metadatas)[0]
