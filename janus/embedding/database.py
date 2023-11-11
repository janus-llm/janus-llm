from pathlib import Path
from urllib.parse import urlparse

import chromadb


class ChromaEmbeddingDatabase(object):
    """Singleton holding a Chroma ClientAPI object.

    Example usage:
    ```
    chroma_client = ChromaEmbeddingDatabase() # Connects to default persistent db directory
    chroma_client.list_collections()

    langchain_collection = langchain.vectorstores.Chroma(
        collection_name="janus",
        client=chroma_client,
        embedding_function=...
    )
    ```
    """
    client = None

    # Common ChromaDB settings
    common_settings = chromadb.config.Settings(
        # Do not report telemetry info
        anonymized_telemetry=False,
        # Allow complete reset of database
        allow_reset=True
    )

    def __new__(cls, path: str | Path = Path.home() / ".janus" / "chroma" / "chroma-data"):
        """Instantiates or returns a Chroma ClientAPI object as configured by the provided path."""
        if cls.client is None:

            # Check if provided path is a URL
            # Assumes that any URLs are strings with a :
            if isinstance(path, str) and ':' in path:
                # urlparse requires a string with a scheme
                if '//' not in path:
                    # ex. localhost:8000 > http://localhost:8000
                    path = f'http://{path}'
                try:
                    parsed_url = urlparse(path)

                    cls.client = chromadb.HttpClient(
                        host=parsed_url.hostname,
                        port=parsed_url.port,
                        settings=cls.common_settings
                    )
                except ValueError:
                    # Invalid url?
                    pass

            else:
                # Is a directory, existing or not
                cls.client = chromadb.PersistentClient(
                    path=path.as_posix() if isinstance(path, Path) else path,
                    settings=cls.common_settings
                )

        return cls.client
