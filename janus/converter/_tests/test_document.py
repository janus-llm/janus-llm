import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from janus.converter.document import ClozeDocumenter, PseudocodeDocumenter
from janus.language.block import CodeBlock, TranslatedCodeBlock


class TestDocumenter(unittest.TestCase):
    """Tests for the Documenter class"""

    @patch("janus.converter.Converter._run_chain")
    def test_cloze(self, mock_run_chain):
        """Test cloze documenter"""
        documenter = ClozeDocumenter(
            model="gpt-4o-mini",
            source_language="ibmhlasm",
            comments_per_request=1,
        )

        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="ibmhlasm",
            text="*\n* <BLOCK_COMMENT 14b80530>\nDFHEISTG DSECT<INLINE_COMMENT dadfa102>",
        )
        source.mark_root()

        mock_run_chain.side_effect = [
            '{"14b80530": "first line"}',
            '{"dadfa102": "second line"}',
        ]

        result = documenter._translate_block(source)

        expected_out = '{"14b80530": "first line", "dadfa102": "second line"}'

        self.assertIsInstance(result, TranslatedCodeBlock)
        self.assertEqual(result.text, expected_out)
        self.assertEqual(result.previous_generation, source.to_janus_object())

    @patch("janus.converter.Converter._run_chain")
    def test_pseudocode(self, mock_run_chain):
        """Test pseudocode documenter"""
        documenter = PseudocodeDocumenter(
            model="gpt-4o-mini",
            source_language="ibmhlasm",
        )

        test_file = Path("janus/language/treesitter/_tests/languages/ibmhlasm.asm")

        with open("janus/converter/_tests/ibmhlasm.json", "r") as f:
            expected = json.load(f)
            mock_run_chain.return_value = expected["output"]

        with tempfile.TemporaryDirectory(dir=test_file.parent) as tmpdir:
            outfile = Path(tmpdir) / test_file.with_suffix(".json").name

            documenter.translate(test_file.parent, tmpdir)

            self.assertTrue(outfile.exists())

            with open(outfile, "r") as f:
                actual = json.load(f)

            # TODO: Really shouldn't have to delete the input metadata here, not
            #       clear what the issue is, something to do with a newline getting
            #       added into the text at some point
            del expected["metadata"]
            del actual["metadata"]
            del expected["input"]["metadata"]
            del actual["input"]["metadata"]
            self.assertEqual(expected, actual)
