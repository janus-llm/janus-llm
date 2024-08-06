import os
from pathlib import Path
from urllib.parse import unquote, urlparse
from urllib.request import url2pathname

import chromadb

from janus.utils.logger import create_logger

log = create_logger(__name__)


# adapted from https://stackoverflow.com/a/61922504
def uri_to_path(uri):
    parsed = urlparse(uri)
    host = "{0}{0}{mnt}{0}".format(os.path.sep, mnt=parsed.netloc)
    return Path(os.path.normpath(os.path.join(host, url2pathname(unquote(parsed.path)))))


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
            if isinstance(path, str):
                parse_result = urlparse(path)
                if len(parse_result.scheme) == 1:
                    # drive letter
                    path = Path(path)
                elif parse_result.scheme == "file":
                    path = uri_to_path(path)
                elif ":" in path or parse_result.scheme in ["http", "https"]:
                    # Otherwise, assumes that any URLs are strings with a :
                    # urlparse requires a string with a scheme
                    if "//" not in path:
                        # ex. localhost:8000 > http://localhost:8000
                        path = f"http://{path}"
                    try:
                        parsed_url = urlparse(path)

                        cls.client = chromadb.HttpClient(
                            host=parsed_url.hostname,
                            port=str(parsed_url.port),
                            settings=cls.common_settings,
                        )
                    except ValueError:
                        message = (
                            f"Invalid URL: {path}, please provide a URL with 'http' "
                        )
                        "or 'https' at the beginning of the string, or provide a port."
                        log.error(message)
                        raise ValueError(message)
                    return cls.client

        # Is a directory, existing or not
        cls.client = chromadb.PersistentClient(
            path=path.as_posix() if isinstance(path, Path) else path,
            settings=cls.common_settings,
        )

        return cls.client
