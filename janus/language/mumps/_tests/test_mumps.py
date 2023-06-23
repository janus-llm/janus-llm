import unittest
from pathlib import Path

from ..mumps import MumpsSplitter


class TestMumpsSplitter(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        self.splitter = MumpsSplitter(max_tokens=2048)
        self.test_file = Path("janus/language/mumps/_tests/test_mumps.m")

    def test_split(self):
        """Test the split method."""
        file = self.splitter.split(self.test_file)
        self.assertEqual(len(file.blocks), 7)
