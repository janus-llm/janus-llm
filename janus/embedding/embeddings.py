import os
from abc import ABC
from typing import Sequence

from chromadb.api import API
from chromadb.api.models.Collection import Collection

from ..utils.enums import EmbeddingType

# See https://docs.trychroma.com/telemetry#in-chromas-backend-using-environment-variables
os.environ["ANONYMIZED_TELEMETRY"] = "False"


class Collections(ABC):
    """Manage embedding collections"""

    def __init__(self, client: API):
        self._client = client

    def create(self, embedding_type: EmbeddingType) -> Collection:
        """Create a Chroma collection for the given embedding type.

        Arguments:
            embedding_type: The type of embedding to create the vector store for
        """
        # First, check if the embedding type exists
        if embedding_type not in EmbeddingType:
            raise ValueError(f"Invalid embedding type: {embedding_type}")
        # Now check if the collection exists
        type_name = embedding_type.name.lower()
        # TODO: do we want to iterate over similarly named collections in other
        #  functions in this codebase?
        similar_collection_names = [
            item.name for item in self.get() if item.name.startswith(type_name)
        ]
        if type_name in similar_collection_names:
            # If it does, create a new collection with a similar but incremented name
            # ex. "requirement" -> "requirement_1"
            # Count the number of collections with the same embedding type
            collection_name = f"{type_name}_{len(similar_collection_names) + 1}"
        else:
            collection_name = type_name
        # TODO: set embedding_function argument to create_collection()
        return self._client.create_collection(collection_name)

    def get(self, name: None | EmbeddingType | str = None) -> Sequence[Collection]:
        """Get the Chroma collections.

        Returns:
            The Chroma collections. Raises ValueError if not found.
        """
        if isinstance(name, str):
            return [self._client.get_collection(name)]
        elif isinstance(name, EmbeddingType):
            return [self._client.get_collection(name.name.lower())]
        else:
            return self._client.list_collections()

    def delete(self) -> None:
        """Delete a Chroma collection"""
        pass
