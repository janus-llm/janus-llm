from abc import ABC, abstractmethod

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import GPT4AllEmbeddings, OpenAIEmbeddings
from langchain.schema.vectorstore import VectorStore
from langchain.vectorstores import Chroma


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

    def create_collection(self, name) -> VectorStore:
        return Chroma(name, self._embeddings)

    def delete_collection(self, vector_store):
        vector_store.delete_collection()


class GPT4AllEmbeddingsFactory(Embeddings):
    def __init__(self):
        self._embeddings = GPT4AllEmbeddings()

    def create_collection(self, name) -> VectorStore:
        return Chroma(name, self._embeddings)

    def delete_collection(self, vector_store):
        vector_store.delete_collection()


def get_embeddings_factory(llm) -> Embeddings:
    """Return an instance of Embeddings based on the current llm type"""
    if isinstance(llm, ChatOpenAI):
        return OpenAIEmbeddingsFactory()
    else:
        return GPT4AllEmbeddingsFactory()
