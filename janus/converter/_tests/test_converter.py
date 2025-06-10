import unittest
from unittest.mock import patch

from janus.converter.converter import Converter
from janus.language.block import CodeBlock
from janus.refiners.refiner import FixParserExceptions


class TestConverter(unittest.TestCase):
    """Tests for the Converter class"""

    def test_load_translation_chain(self):
        converter = Converter(
            model="gpt-4o",
            source_language="json",
            refiner_types=[FixParserExceptions],
            prompt_template="simple",
            use_janus_inputs=True,
        )

        converter._load_parameters()

        self.assertEqual(5, len(converter._chain.steps))

    @patch("janus.converter.Converter._run_chain")
    def test_iterative_translate(self, mock_run_chain):
        converter = Converter(
            model="gpt-4o",
            source_language="json",
            refiner_types=[FixParserExceptions],
            use_janus_inputs=True,
        )

        source = CodeBlock(
            id="root",
            name="root",
            node_type="root",
            language="plaintext",
            children=[
                CodeBlock(
                    id="child a",
                    name="child a",
                    node_type="child",
                    language="plaintext",
                    text="first child",
                    affixes=("[prefix a]\n  ", "\n[suffix a]\n  "),
                ),
                CodeBlock(
                    id="child b",
                    name="child b",
                    node_type="child",
                    language="plaintext",
                    text="second child",
                    affixes=("\n[prefix b]\n  ", "\n[suffix b]"),
                ),
            ],
            text=None,
            affixes=("[prefix]\n", "\n[suffix]"),
        )
        source.mark_root()

        mock_run_chain.side_effect = ["first output", "second output"]

        translated = converter._translate_block(source)

        self.assertEqual("first output", translated.children[0].text)
        self.assertEqual("second output", translated.children[1].text)

        prefix = "[prefix]\n[prefix a]\n  "
        central = "first output\n[suffix a]\n  second output"
        suffix = "\n[suffix b]\n[suffix]"
        self.assertEqual(f"{prefix}{central}{suffix}", translated.complete_text)
