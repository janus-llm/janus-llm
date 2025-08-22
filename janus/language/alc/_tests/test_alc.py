import unittest
from pathlib import Path

from janus.language.alc import AlcRegexSplitter, AlcSplitter
from janus.language.combine import Combiner, UnorderedTreeCombiner
from janus.llm import load_model


class TestAlcSplitter(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        model_name = "gpt-4o"
        llm = load_model(model_name)
        self.splitter = AlcSplitter(model=llm)
        self.regex_splitter = AlcRegexSplitter(
            model=llm, skip_merge=True, max_tokens=int(1e12)
        )
        self.combiner = Combiner(language="ibmhlasm")
        self.regex_combiner = UnorderedTreeCombiner(language="ibmhlasm")
        self.test_file = Path("janus/language/alc/_tests/alc.asm")

    def test_split(self):
        """Test the split method."""
        tree_root = self.splitter.split(self.test_file)
        self.assertAlmostEqual(tree_root.n_descendents, 16, delta=2)
        self.assertLessEqual(tree_root.max_tokens, self.splitter.max_tokens)
        self.assertFalse(tree_root.complete)
        self.combiner.combine_children(tree_root)
        self.assertTrue(tree_root.complete)
        self.assertEqual(tree_root.complete_text, self.test_file.read_text())

    def test_regex_split(self):
        """Test the split method."""
        tree_root = self.regex_splitter.split(self.test_file)
        self.assertAlmostEqual(tree_root.n_descendents, 492, delta=2)
        self.assertFalse(tree_root.complete)
        self.regex_combiner.combine(tree_root)
        self.assertTrue(tree_root.complete)
        self.assertEqual(tree_root.complete_text, self.test_file.read_text())
