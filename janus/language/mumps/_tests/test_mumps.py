import unittest
from pathlib import Path

from ..mumps import MumpsSplitter
from ....llm import MODEL_CONSTRUCTORS, MODEL_DEFAULT_ARGUMENTS


class TestMumpsSplitter(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        model_name = "gpt-3.5-turbo"
        llm = MODEL_CONSTRUCTORS[model_name](**MODEL_DEFAULT_ARGUMENTS[model_name])
        self.splitter = MumpsSplitter(model=llm, max_tokens=2048)
        self.test_file = Path("janus/language/mumps/_tests/test_mumps.m")

    def test_split(self):
        """Test the split method."""
        block = self.splitter.split(self.test_file)
        self.assertEqual(len(block.children), 23)
