import unittest
from pathlib import Path

import pytest

from ..translate import Translator


class TestTranslator(unittest.TestCase):
    """Tests for the Translator class."""

    def setUp(self):
        """Set up the tests."""
        self.translator = Translator(
            model="gpt-3.5-turbo",
            source_language="fortran",
            target_language="python",
            target_version="3.10",
        )
        self.test_file = Path("janus/language/treesitter/_tests/languages/fortran.f90")

    def test_translate(self):
        """Test the translate method."""
        # Delete a file if it's already there
        python_file = self.test_file.parent / "python" / f"{self.test_file.stem}.py"
        costs_file = self.test_file.parent / "python" / "costs.csv"
        costs_file.unlink(missing_ok=True)
        python_file.unlink(missing_ok=True)
        python_file.parent.rmdir() if python_file.parent.is_dir() else None
        self.translator.translate(self.test_file.parent, self.test_file.parent / "python")
        # Only check the top-most level functionality, since it should be handled by other
        # unit tests anyway
        self.assertTrue(python_file.exists())


@pytest.mark.parametrize(
    "prompt_template,expected_target_language",
    [
        ("document_inline", "python"),
        ("document", "text"),
        ("requirements", "text"),
        ("simple", "javascript"),
    ],
)
def test_target_language(prompt_template, expected_target_language):
    """Tests that translator target language settings are consistent
    with prompt template expectations.
    """
    translator = Translator(
        source_language="python",
        target_language="javascript",
        prompt_template=prompt_template,
    )
    assert translator.target_language == expected_target_language
    assert translator.combiner.language == expected_target_language
    assert translator.parser.target_language == expected_target_language
