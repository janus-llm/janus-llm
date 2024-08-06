import unittest
from pathlib import Path

from janus.language.combine import Combiner
from janus.language.mumps import MumpsSplitter
from janus.llm import load_model


class TestMumpsSplitter(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        model_name = "gpt-4o"
        llm, _, _, _ = load_model(model_name)
        self.splitter = MumpsSplitter(model=llm)
        self.combiner = Combiner(language="mumps")
        self.test_file = Path("janus/language/mumps/_tests/mumps.m")

    def test_split(self):
        """Test the split method."""
        tree_root = self.splitter.split(self.test_file)
        self.assertEqual(len(tree_root.children), 22)
        self.assertLessEqual(tree_root.max_tokens, self.splitter.max_tokens)
        self.assertFalse(tree_root.complete)
        self.combiner.combine_children(tree_root)
        self.assertTrue(tree_root.complete)
        self.assertEqual(tree_root.complete_text, self.test_file.read_text())
