from pathlib import Path
from urllib.parse import urlparse

import chromadb

from ..utils.logger import create_logger

log = create_logger(__name__)


class ChromaEmbeddingDatabase(object):
    """Singleton holding a Chroma ClientAPI object.

    Example usage:
    ```
    # Connects to default persistent db directory
    chroma_client = ChromaEmbeddingDatabase()
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
        allow_reset=True,
    )

    def __new__(
        cls, path: str | Path = Path.home() / ".janus" / "chroma" / "chroma-data"
    ):
        """Instantiates or returns a Chroma ClientAPI object as configured by the
        provided path.

        Arguments:
            path: The path to the ChromaDB. Can be either a string of a URL or path or a
                Path object.

        Returns:
            A Chroma ClientAPI object.
        """
        if cls.client is None:
            # Check if provided path is a URL
            # Assumes that any URLs are strings with a :
            if isinstance(path, str) and (
                ":" in path or urlparse(path).scheme in ["http", "https"]
            ):
                # urlparse requires a string with a scheme
                if "//" not in path:
                    # ex. localhost:8000 > http://localhost:8000
                    path = f"http://{path}"
                try:
                    parsed_url = urlparse(path)

                    cls.client = chromadb.HttpClient(
                        host=parsed_url.hostname,
                        port=parsed_url.port,
                        settings=cls.common_settings,
                    )
                except ValueError:
                    message = f"Invalid URL: {path}, please provide a URL with 'http' "
                    "or 'https' at the beginning of the string, or provide a port."
                    log.error(message)
                    raise ValueError(message)

            else:
                # Is a directory, existing or not
                cls.client = chromadb.PersistentClient(
                    path=path.as_posix() if isinstance(path, Path) else path,
                    settings=cls.common_settings,
                )

        return cls.client
