import unittest
from pathlib import Path

from ..fortran import FortranSplitter
from ..node import NODE_TYPES


class TestFortranSplitter(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        self.splitter = FortranSplitter(NODE_TYPES)
        self.test_file = Path("janus/language/fortran/_tests/test_fortran.f90")

    def test_split(self):
        """Test the split method."""
        split_code = self.splitter.split(self.test_file)
        self.assertEqual(len(split_code), 7)
