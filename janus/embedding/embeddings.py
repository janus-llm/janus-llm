import os
from abc import ABC, abstractmethod

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import GPT4AllEmbeddings, OpenAIEmbeddings
from langchain.llms import HuggingFaceTextGenInference
from langchain.schema.embeddings import Embeddings

# See https://docs.trychroma.com/telemetry#in-chromas-backend-using-environment-variables
os.environ["ANONYMIZED_TELEMETRY"] = "False"


class EmbeddingsFactory(ABC):
    """Manage lifecycle of embedding collections"""

    @abstractmethod
    def get_embeddings(self) -> Embeddings:
        """Getter"""


class OpenAIEmbeddingsFactory(EmbeddingsFactory):
    def __init__(self):
        self._embeddings = OpenAIEmbeddings(disallowed_special=())

    def get_embeddings(self) -> Embeddings:
        return self._embeddings


class GPT4AllEmbeddingsFactory(EmbeddingsFactory):
    def __init__(self):
        self._embeddings = GPT4AllEmbeddings()

    def get_embeddings(self) -> Embeddings:
        return self._embeddings


def get_embeddings(llm: ChatOpenAI | HuggingFaceTextGenInference) -> Embeddings:
    """Return an instance of Embeddings based on the current `llm` type

    Arguments:
        llm: The llm instance to use

    Returns:
        An Embeddings instance
    """
    if llm in ["text-embedding-ada-002", "openai"]:
        return OpenAIEmbeddingsFactory().get_embeddings()
    else:
        return GPT4AllEmbeddingsFactory().get_embeddings()
