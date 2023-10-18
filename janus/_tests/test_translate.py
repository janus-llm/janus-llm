import unittest
from pathlib import Path

import pytest

from ..translate import Translator


class TestTranslator(unittest.TestCase):
    """Tests for the Translator class."""

    def setUp(self):
        """Set up the tests."""
        self.translator = Translator(
            model="gpt-3.5-turbo",
            source_language="fortran",
            target_language="python",
            target_version="3.10",
        )
        self.test_file = Path("janus/language/treesitter/_tests/languages/fortran.f90")

    def test_translate(self):
        """Test the translate method."""
        # Delete a file if it's already there
        python_file = self.test_file.parent / "python" / f"{self.test_file.stem}.py"
        costs_file = self.test_file.parent / "python" / "costs.csv"
        costs_file.unlink(missing_ok=True)
        python_file.unlink(missing_ok=True)
        python_file.parent.rmdir() if python_file.parent.is_dir() else None
        self.translator.translate(self.test_file.parent, self.test_file.parent / "python")
        # Only check the top-most level functionality, since it should be handled by other
        # unit tests anyway
        self.assertTrue(python_file.exists())

    def test_invalid_selections(self) -> None:
        """Tests that settings values for the translator will raise exceptions"""
        self.assertRaises(
            ValueError, self.translator.set_target_language, "gobbledy", "goobledy"
        )
        self.assertRaises(ValueError, self.translator.set_parser_type, "blah")
        self.assertRaises(
            ValueError, self.translator.set_source_language, "scribbledy-doop"
        )
        self.translator.set_prompt("pish posh")
        self.assertRaises(ValueError, self.translator._load_parameters)


@pytest.mark.parametrize(
    "source_language,prompt_template,expected_target_language,expected_target_version,"
    "parser_type",
    [
        ("python", "document_inline", "python", "3.10", "code"),
        ("fortran", "document", "text", None, "text"),
        ("mumps", "requirements", "text", None, "text"),
        ("python", "simple", "javascript", "es6", "code"),
    ],
)
def test_language_combinations(
    source_language: str,
    prompt_template: str,
    expected_target_language: str,
    expected_target_version: str,
    parser_type: str,
):
    """Tests that translator target language settings are consistent
    with prompt template expectations.
    """
    translator = Translator(model="gpt-3.5-turbo")
    translator.set_model("gpt-3.5-turbo-16k")
    translator.set_source_language(source_language)
    translator.set_target_language(expected_target_language, expected_target_version)
    translator.set_parser_type(parser_type)
    translator.set_prompt(prompt_template)
    translator._load_parameters()
    assert translator._target_language == expected_target_language
    assert translator._target_version == expected_target_version
    assert translator._parser_type == parser_type
    assert translator.splitter.language == source_language
    assert translator.splitter.model.model_name == "gpt-3.5-turbo-16k"
    assert translator._prompt_engine._template_name == prompt_template
