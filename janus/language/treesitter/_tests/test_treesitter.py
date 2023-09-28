import unittest
from pathlib import Path

from ....llm import MODEL_CONSTRUCTORS, MODEL_DEFAULT_ARGUMENTS
from ...combine import Combiner
from ..treesitter import TreeSitterSplitter


class TestTreeSitterSplitter(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        model_name = "gpt-3.5-turbo"
        self.llm = MODEL_CONSTRUCTORS[model_name](**MODEL_DEFAULT_ARGUMENTS[model_name])

    def _split(self):
        """Split the test file."""
        tree_root = self.splitter.split(self.test_file)
        self.assertFalse(tree_root.complete)
        self.combiner.combine(tree_root)
        self.assertTrue(tree_root.complete)
        split_text = tree_root.text
        # The newlines and spaces aren't the same but that doesn't matter for fortran
        # (to an extent)
        self.assertEqual(split_text, self.test_file.read_text())

    def test_split_fortran(self):
        """Test the split method."""
        self.splitter = TreeSitterSplitter(language="fortran", model=self.llm)
        self.combiner = Combiner(language="fortran")
        self.test_file = Path("janus/language/treesitter/_tests/languages/fortran.f90")
        self.splitter.use_placeholders = False
        self._split()

        self.splitter.use_placeholders = True
        self._split()

    def test_split_matlab(self):
        """Test the split method."""
        self.splitter = TreeSitterSplitter(language="matlab", model=self.llm)
        self.combiner = Combiner(language="matlab")
        self.test_file = Path("janus/language/treesitter/_tests/languages/matlab.m")
        self._split()

        self.splitter.use_placeholders = False
        self._split()
