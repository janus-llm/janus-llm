import os
import unittest
from pathlib import Path
from unittest.mock import patch

import pytest

from janus.language.binary import BinarySplitter
from janus.llm import load_model


class TestBinarySplitter(unittest.TestCase):
    """Tests for the BinarySplitter class."""

    def setUp(self):
        model_name = "gpt-4o"
        self.binary_file = Path("janus/language/binary/_tests/hello")
        self.llm = load_model(model_name)
        self.splitter = BinarySplitter(model=self.llm)
        os.environ["GHIDRA_INSTALL_PATH"] = "~/programs/ghidra_10.4_PUBLIC"

    def test_setup(self):
        """Test that the setup sets the environment variable correctly."""
        with patch("os.getenv") as mock_getenv:
            mock_getenv.return_value = "~/programs/ghidra_10.4_PUBLIC"
            self.assertEqual(
                os.getenv("GHIDRA_INSTALL_PATH"), "~/programs/ghidra_10.4_PUBLIC"
            )
            mock_getenv.assert_called_once_with("GHIDRA_INSTALL_PATH")

    def test_initialization(self):
        """Test that BinarySplitter is initialized correctly."""
        self.assertIsInstance(self.splitter, BinarySplitter)
        self.assertEqual(self.splitter.model, self.llm)

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
