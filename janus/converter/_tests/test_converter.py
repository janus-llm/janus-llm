import unittest
from unittest.mock import patch

from janus.converter.converter import Converter
from janus.language.block import CodeBlock
from janus.refiners.refiner import FixParserExceptions


class TestConverter(unittest.TestCase):
    """Tests for the Converter class"""

    def setUp(self):
        """Set up the tests"""
        self.converter = Converter(
            model="gpt-4o",
            source_language="json",
            refiner_types=[FixParserExceptions],
            use_janus_inputs=True,
        )

    def test_load_translation_chain(self):
        self.converter._prompt_template_names = ["simple", "pseudocode"]

        self.converter._load_translation_chain()

        self.assertEqual(4, len(self.converter._translation_chain.steps))

    @patch("janus.converter.Converter._run_chain")
    def test_iterative_translate(self, mock_run_chain):
        source = CodeBlock(
            id="test",
            name="Test Block",
            node_type="function",
            language="json",
            text="This is UML",
            start_point=(0, 0),
            end_point=(1, 0),
            start_byte=0,
            end_byte=1,
            tokens=5,
            children=[
                CodeBlock(
                    id="test2",
                    name="Test Block",
                    node_type="function",
                    language="json",
                    text="This is UML",
                    start_point=(0, 0),
                    end_point=(1, 0),
                    start_byte=0,
                    end_byte=1,
                    tokens=5,
                    children=[],
                    previous_generations=[],
                )
            ],
            previous_generations=[{"input": "test"}],
        )

        mock_run_chain.side_effect = ['{"a":"b"}', '{"c":"d"}']

        translated = self.converter._iterative_translate(source)

        self.assertEqual('{"a":"b"}', translated.text)
        self.assertEqual('{"c":"d"}', translated.children[0].text)

    def test_janus_object_to_codeblock(self):
        obj = {
            "input": "hello",
            "outputs": ["welcome", "world"],
            "metadata": {
                "cost": 3,
                "processing_time": 1,
                "num_requests": 1,
                "input_tokens": 0,
                "output_tokens": 0,
                "converter_name": "Documenter",
                "type": "documentation",
                "label": None,
            },
        }

        actual = self.converter._janus_object_to_codeblock(obj, "name")

        self.assertEqual("welcome", actual.blocks[0].text)
        self.assertEqual("world", actual.blocks[1].text)
