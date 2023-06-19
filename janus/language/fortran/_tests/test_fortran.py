import unittest
from pathlib import Path

from ..fortran import FortranSplitter


class TestFortranSplitter(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        self.splitter = FortranSplitter()
        self.test_file = Path("janus/language/fortran/_tests/test_fortran.f90")

    def test_split(self):
        """Test the split method."""
        split_code = self.splitter.split(self.test_file)
        flat_split_text = self.splitter._blocks_to_str(split_code.code, split_code)
        # The newlines and spaces aren't the same but that doesn't matter for fortran
        # (to an extent)
        flat_split_text = flat_split_text.replace("\n", "").replace(" ", "")
        test_file_replaced = self.test_file.read_text().replace("\n", "").replace(" ", "")
        self.assertEqual(flat_split_text, test_file_replaced)
