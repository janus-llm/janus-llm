import unittest
from pathlib import Path

from ..translate import Translator


class TestTranslator(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        self.translator = Translator("gpt-3.5-turbo", "fortran", "python", "3.10")
        self.test_file = Path("janus/language/fortran/_tests/fortran.f90")

    def test_translate(self):
        """Test the split method."""
        # Delete a file if it's already there
        python_file = self.test_file.parent / "python" / f"{self.test_file.stem}.py"
        python_file.unlink(missing_ok=True)
        python_file.parent.rmdir() if python_file.parent.is_dir() else None
        self.translator.translate(self.test_file.parent, self.test_file.parent / "python")
        # Only check the top-most level functionality, since it should be handled by other
        # unit tests anyway
        self.assertTrue(python_file.exists())
