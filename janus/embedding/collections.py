import datetime
import os
from typing import Sequence

from chromadb import Client, Collection

from ..utils.enums import EmbeddingType

# See https://docs.trychroma.com/telemetry#in-chromas-backend-using-environment-variables
os.environ["ANONYMIZED_TELEMETRY"] = "False"


class Collections:
    """Manage embedding collections"""

    def __init__(self, client: Client):
        self._client = client

    def create(self, name: EmbeddingType | str) -> Collection:
        """Create a Chroma collection for the given embedding type.

        Arguments:
            embedding_type: The type of embedding to create the vector store for
        """
        collection_name = self._set_collection_name(name)
        metadata = {
            "date_created": datetime.datetime.now().date().isoformat(),
            "time_created": datetime.datetime.now().time().isoformat(),
        }
        return self._client.create_collection(collection_name, metadata=metadata)

    def get_or_create(self, name: EmbeddingType | str) -> Collection:
        """Create a Chroma collection for the given embedding type.

        Arguments:
            embedding_type: The type of embedding to create the vector store for
        """
        collection_name = self._set_collection_name(name)
        metadata = {
            "date_created": datetime.datetime.now().date().isoformat(),
            "time_created": datetime.datetime.now().time().isoformat(),
        }
        return self._client.get_or_create_collection(collection_name, metadata=metadata)

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

    def delete(self, name: EmbeddingType | str) -> None:
        """Delete a Chroma collection"""
        if isinstance(name, EmbeddingType):
            collection_name = name.name.lower()
        else:
            collection_name = name
        self._client.delete_collection(collection_name)

    def _set_collection_name(self, name: EmbeddingType | str) -> str:
        """Set the collection name based on the embedding type"""
        if isinstance(name, EmbeddingType):
            # First, check if the embedding type exists
            if name not in EmbeddingType:
                raise ValueError(f"Invalid embedding type: {name}")
            # Now check if the collection exists
            type_name = name.name.lower()
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
                collection_name = f"{type_name}_1"
            # TODO: set embedding_function argument to create_collection()
        else:
            collection_name = name
        return collection_name
