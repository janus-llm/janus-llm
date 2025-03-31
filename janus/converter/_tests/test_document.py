import tempfile
import unittest
from pathlib import Path

import pytest

from janus.converter.document import PseudocodeDocumenter


class TestDocumenter(unittest.TestCase):
    """Tests for the Documenter class"""

    @pytest.mark.translate
    def test_pseudocode(self):
        """Test pseudocode documenter"""
        test_file = Path("janus/language/treesitter/_tests/languages/ibmhlasm.asm")

        with tempfile.TemporaryDirectory(dir=test_file.parent) as tmpdirname:
            python_file = Path(tmpdirname) / f"{test_file.stem}.json"

            documenter = PseudocodeDocumenter(
                model="gpt-4o-mini", source_language="ibmhlasm"
            )
            documenter.translate(test_file.parent, tmpdirname)
            # Only check the top-most level functionality,
            # since it should be handled by other unit tests anyway
            self.assertTrue(python_file.exists())
