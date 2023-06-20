import unittest
from pathlib import Path

from ..translate import Translator


class TestTranslator(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        self.translator = Translator("gpt-3.5-turbo", "fortran", "python", "3.10")
        self.test_file = Path("janus/language/fortran/_tests/test_fortran.f90")

    def test_translate(self):
        """Test the split method."""
        self.translator.translate(self.test_file.parent, self.test_file.parent / "python")
        self.assertTrue(True)
