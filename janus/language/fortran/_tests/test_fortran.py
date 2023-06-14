import unittest
from pathlib import Path

from ..fortran import FortranSplitter
from ..patterns import NODE_TYPES


class TestFortranSplitter(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        self.splitter = FortranSplitter(NODE_TYPES, max_tokens=4096)
        self.test_file = Path("janus/language/fortran/_tests/test_fortran.f90")

    def test_split(self):
        """Test the split method."""
        with open(self.test_file, "r") as f:
            code = f.read()
        split_code = self.splitter(code)
        self.assertEqual(len(split_code), 7)
