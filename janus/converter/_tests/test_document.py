import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from janus.converter.document import ClozeDocumenter, PseudocodeDocumenter
from janus.language.block import CodeBlock, TranslatedCodeBlock


class TestDocumenter(unittest.TestCase):
    """Tests for the Documenter class"""

    @patch("janus.converter.Converter._add_translation")
    @patch("janus.parsers.doc_parser.ClozeDocumentationParser.parse")
    def test_cloze(self, mock_parse, mock_super_add_translation):
        """Test cloze documenter"""
        documenter = ClozeDocumenter(model="gpt-4o-mini", source_language="ibmhlasm")
        documenter.comments_per_request = 1

        code_block = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="ibmhlasm",
            text="*\n* <BLOCK_COMMENT 14b80530>\nDFHEISTG DSECT<INLINE_COMMENT dadfa102>",
            start_point=(0, 0),
            end_point=(1, 0),
            start_byte=0,
            end_byte=1,
            tokens=0,
            children=[],
            previous_generations=[],
        )

        mock_super_add_translation.return_value = None

        mock_parse.side_effect = [
            '{"14b80530": "first line"}',
            '{"dadfa102": "second line"}',
            "{}",
        ]

        documenter._add_translation(
            TranslatedCodeBlock(code_block, documenter.target_language, documenter)
        )

        self.assertEqual(3, mock_parse.call_count)

        expectedJsonObj = '{"14b80530": "first line", "dadfa102": "second line"}'

        # verify that comments are joined back together properly
        mock_parse.assert_called_with(expectedJsonObj)

    @patch("janus.converter.Converter._run_chain")
    @patch("time.time")
    def test_pseudocode(self, mock_time, mock_run_chain):
        """Test pseudocode documenter"""
        mock_time.return_value = 1

        test_file = Path("janus/language/treesitter/_tests/languages/ibmhlasm.asm")

        with open("janus/converter/_tests/test_document_llm_response.txt", "r") as f:
            mock_run_chain.return_value = f.read()

        with tempfile.TemporaryDirectory(dir=test_file.parent) as tmpdirname:
            python_file = Path(tmpdirname) / f"{test_file.stem}.json"

            documenter = PseudocodeDocumenter(
                model="gpt-4o-mini", source_language="ibmhlasm"
            )
            documenter.translate(test_file.parent, tmpdirname)

            with open("janus/converter/_tests/test_document_expected.json", "r") as f:
                expected = json.load(f)

            with open(python_file, "r") as f:
                actual = json.load(f)

            self.assertEqual(expected, actual)
