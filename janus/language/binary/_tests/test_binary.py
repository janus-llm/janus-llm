import os
import unittest
from pathlib import Path

import pytest

from ....llm import load_model
from ..binary import BinarySplitter


class TestBinarySplitter(unittest.TestCase):
    """Tests for the BinarySplitter class."""

    def setUp(self):
        model_name = "gpt-3.5-turbo"
        self.binary_file = Path("janus/language/binary/_tests/hello")
        self.llm, _, _ = load_model(model_name)
        self.splitter = BinarySplitter(model=self.llm)
        os.environ["GHIDRA_INSTALL_PATH"] = "~/programs/ghidra_10.4_PUBLIC"

    @pytest.mark.ghidra(
        reason=(
            "No way to test this in CI w/o installing Ghidra, but want to keep here to "
            "run manually."
        )
    )
    def test__get_decompilation(self) -> None:
        """Test that _get_decompilation returns a string."""
        decompiled: str = (
            '\nundefined4 entry(void)\n\n{\n  _printf("Hello, World!");\n  '
            "return 0;\n}\n\n"
        )
        self.assertEqual(self.splitter._get_decompilation(self.binary_file), decompiled)
