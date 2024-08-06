import unittest
from pathlib import Path
from unittest.mock import patch

from janus.embedding.database import ChromaEmbeddingDatabase, uri_to_path


class TestDatabase(unittest.TestCase):
    def test_uri_to_path(self):
        uri = (Path.home().expanduser() / "Documents" / "testfile.txt").as_uri()
        expected_path = Path.home().expanduser() / "Documents" / "testfile.txt"
        self.assertEqual(uri_to_path(uri), expected_path)

    @patch("chromadb.PersistentClient", autospec=True)
    def test_ChromaEmbeddingDatabase(self, mock_client):
        # Test with default path
        _ = ChromaEmbeddingDatabase()
        mock_client.assert_called_once()

        # Test with custom path
        custom_path = "/custom/path/to/chroma-data"
        _ = ChromaEmbeddingDatabase(custom_path)
        mock_client.assert_called()

        # Test with URL
        url = "http://example.com/chroma-data"
        _ = ChromaEmbeddingDatabase(url)
        mock_client.assert_called()


if __name__ == "__main__":
    unittest.main()
