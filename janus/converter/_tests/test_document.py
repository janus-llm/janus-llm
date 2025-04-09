import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from janus.converter.document import PseudocodeDocumenter


class TestDocumenter(unittest.TestCase):
    """Tests for the Documenter class"""

    @patch("janus.converter.Converter._run_chain")
    @patch("time.time")
    def test_pseudocode(self, mock_time, mock_translate):
        """Test pseudocode documenter"""
        mock_time.return_value = 1

        test_file = Path("janus/language/treesitter/_tests/languages/ibmhlasm.asm")

        with open("janus/converter/_tests/test_document_llm_response.txt", "r") as f:
            mock_translate.return_value = f.read()

        with tempfile.TemporaryDirectory(dir=test_file.parent) as tmpdirname:
            python_file = Path(tmpdirname) / f"{test_file.stem}.json"

            documenter = PseudocodeDocumenter(
                model="gpt-4o-mini", source_language="ibmhlasm"
            )
            documenter.translate(test_file.parent, tmpdirname)

            with open("janus/converter/_tests/test_document_expected.json", "r") as f:
                expected = json.load(f)

            with open(python_file, "r") as f:
                actual = json.load(f)

            self.assertEqual(expected, actual)
