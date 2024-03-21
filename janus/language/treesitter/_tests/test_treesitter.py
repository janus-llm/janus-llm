import unittest
from pathlib import Path

from ....llm import load_model
from ...combine import Combiner
from ..treesitter import TreeSitterSplitter


class TestTreeSitterSplitter(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        model_name = "gpt-3.5-turbo"
        self.maxDiff = None
        self.llm, _, _ = load_model(model_name)

    def _split(self):
        """Split the test file."""
        tree_root = self.splitter.split(self.test_file)
        self.assertFalse(tree_root.complete)
        self.assertLessEqual(tree_root.max_tokens, self.splitter.max_tokens)
        self.combiner.combine(tree_root)
        self.assertTrue(tree_root.complete)
        self.assertEqual(tree_root.complete_text, self.test_file.read_text())

    def test_split_fortran(self):
        """Test the split method."""
        self.splitter = TreeSitterSplitter(language="fortran", model=self.llm)
        self.combiner = Combiner(language="fortran")
        self.test_file = Path("janus/language/treesitter/_tests/languages/fortran.f90")
        self._split()

    def test_split_ibmhlasm(self):
        """Test the split method."""
        self.splitter = TreeSitterSplitter(
            language="ibmhlasm", model=self.llm, max_tokens=100
        )
        self.combiner = Combiner(language="ibmhlasm")
        self.test_file = Path("janus/language/treesitter/_tests/languages/ibmhlasm.asm")
        self._split()

    def test_split_matlab(self):
        """Test the split method."""
        self.splitter = TreeSitterSplitter(
            language="matlab",
            model=self.llm,
            max_tokens=(4096 // 3),
            # max_tokens used to be / 3 always in TreeSitterSplitter to leave just as
            # much space for the prompt as for the translated code.
        )
        self.combiner = Combiner(language="matlab")
        self.test_file = Path("janus/language/treesitter/_tests/languages/matlab.m")
        self._split()
