import unittest

from janus.parsers.code_parser import CodeParser
from janus.parsers.parser import GenericParser


class TestJanusParser(unittest.TestCase):
    def setUp(self):
        self.parser = GenericParser()

    def test_parse_combined_output(self):
        text = "test text"
        self.assertEqual(self.parser.parse_combined_output(text), text)


class TestCodeParser(unittest.TestCase):
    def setUp(self):
        self.parser = CodeParser(language="python")

    def test_parse(self):
        self.parser.language = "python"
        text = "```\n# test text\n```"
        self.assertEqual(self.parser.parse(text), text.strip("```").strip("\n"))

    def test_get_format_instructions(self):
        self.assertEqual(
            self.parser.get_format_instructions(),
            "Output must contain text contained within triple square brackets (```)",
        )


if __name__ == "__main__":
    unittest.main()
