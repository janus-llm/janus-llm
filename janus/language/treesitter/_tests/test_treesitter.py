import unittest
from pathlib import Path

from ....llm import MODEL_CONSTRUCTORS, MODEL_DEFAULT_ARGUMENTS
from ..treesitter import TreeSitterSplitter


class TestTreeSitterSplitter(unittest.TestCase):
    """Tests for the Splitter class."""

    def setUp(self):
        """Set up the tests."""
        model_name = "gpt-3.5-turbo"
        self.llm = MODEL_CONSTRUCTORS[model_name](**MODEL_DEFAULT_ARGUMENTS[model_name])

    def _split(self) -> str:
        """Split the test file."""
        split_code = self.splitter.split(self.test_file)
        flat_split_text = self.splitter._blocks_to_str(split_code.code, split_code)
        # The newlines and spaces aren't the same but that doesn't matter for fortran
        # (to an extent)
        flat_split_text = flat_split_text.replace("\n", "").replace(" ", "")
        test_file_replaced = self.test_file.read_text().replace("\n", "").replace(" ", "")
        self.assertEqual(flat_split_text, test_file_replaced)

    def test_split_fortran(self):
        """Test the split method."""
        self.splitter = TreeSitterSplitter(language="fortran", model=self.llm)
        self.test_file = Path("janus/language/treesitter/_tests/languages/fortran.f90")
        self._split()

    def test_split_matlab(self):
        """Test the split method."""
        self.splitter = TreeSitterSplitter(language="matlab", model=self.llm)
        self.test_file = Path("janus/language/treesitter/_tests/languages/matlab.m")
        self._split()
