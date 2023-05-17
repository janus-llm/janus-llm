import unittest
from pathlib import Path

from ..fortran import FortranSplitter


class TestFortranSplitter(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        self.splitter = FortranSplitter()
        self.test_file = Path("janus/language/_tests/test_fortran.f90")

    def test_split(self):
        """Test the split method."""
        file = self.splitter.split(self.test_file)
        self.assertEqual(len(file.blocks), 1)
