import os
from abc import ABC, abstractmethod

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import GPT4AllEmbeddings, OpenAIEmbeddings
from langchain.llms import HuggingFaceTextGenInference
from langchain.schema.vectorstore import VectorStore
from langchain.vectorstores import Chroma

# See https://docs.trychroma.com/telemetry#in-chromas-backend-using-environment-variables
os.environ["ANONYMIZED_TELEMETRY"] = "False"


class Embeddings(ABC):
    """Manage lifecycle of embeddings"""

    @abstractmethod
    def create_collection(self, name) -> VectorStore:
        """Factory method"""

    @abstractmethod
    def delete_collection(self, vector_store):
        """Factory method"""


class OpenAIEmbeddingsFactory(Embeddings):
    def __init__(self):
        self._embeddings = OpenAIEmbeddings(disallowed_special=())

    def create_collection(self, name: str) -> VectorStore:
        """Factory method for creating a VectorStore instance

        Arguments:
            name: The name of the collection

        Returns:
            A VectorStore instance with the given collection name
        """
        return Chroma(name, self._embeddings)

    def delete_collection(self, vector_store: VectorStore) -> None:
        """Delete a collection

        Arguments:
            vector_store: The VectorStore instance to delete
        """
        vector_store.delete_collection()


class GPT4AllEmbeddingsFactory(Embeddings):
    def __init__(self):
        self._embeddings = GPT4AllEmbeddings()

    def create_collection(self, name: str) -> VectorStore:
        """Factory method for creating a VectorStore instance

        Arguments:
            name: The name of the collection

        Returns:
            A VectorStore instance with the given collection name
        """
        return Chroma(name, self._embeddings)

    def delete_collection(self, vector_store: VectorStore) -> None:
        """Delete a collection

        Arguments:
            vector_store: The VectorStore instance to delete
        """
        vector_store.delete_collection()


def get_embeddings(llm: ChatOpenAI | HuggingFaceTextGenInference) -> Embeddings:
    """Return an instance of Embeddings based on the current `llm` type

    Arguments:
        llm: The llm instance to use

    Returns:
        An Embeddings instance
    """
    if llm in ["text-embedding-ada-002", "openai"]:
        return OpenAIEmbeddingsFactory()._embeddings
    else:
        return GPT4AllEmbeddingsFactory()._embeddings
