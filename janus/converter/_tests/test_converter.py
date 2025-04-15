import unittest

from janus.converter.converter import Converter
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
