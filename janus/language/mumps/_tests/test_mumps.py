import unittest
from pathlib import Path

from ....llm import MODEL_CONSTRUCTORS, MODEL_DEFAULT_ARGUMENTS
from ..mumps import MumpsSplitter
from ...combine import Combiner


class TestMumpsSplitter(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        model_name = "gpt-3.5-turbo"
        llm = MODEL_CONSTRUCTORS[model_name](**MODEL_DEFAULT_ARGUMENTS[model_name])
        self.splitter = MumpsSplitter(model=llm, max_tokens=2048)
        self.combiner = Combiner(language="mumps")
        self.test_file = Path("janus/language/mumps/_tests/mumps.m")

    def test_split(self):
        """Test the split method."""
        split_code = self.splitter.split(self.test_file)
        self.assertEqual(len(split_code.children), 22)
        flat_split_text = self.combiner._blocks_to_str(split_code.code, split_code)
        self.assertEqual(flat_split_text, self.test_file.read_text())
