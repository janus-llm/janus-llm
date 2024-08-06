# FILEPATH: /Users/mdoyle/projects/janus/janus/metrics/tests/test_file_pairing.py

import unittest
from pathlib import Path

from janus.metrics.file_pairing import (
    FILE_PAIRING_METHODS,
    pair_by_file,
    pair_by_line,
    pair_by_line_comment,
    register_pairing_method,
)


class TestFilePairing(unittest.TestCase):
    def setUp(self):
        self.src = "Hello\nWorld"
        self.cmp = "Hello\nPython"
        self.state = {
            "token_limit": 100,
            "llm": None,
            "lang": "python",
            "target_file": self.src,
            "cmp_file": self.cmp,
        }

    def test_register_pairing_method(self):
        @register_pairing_method(name="test")
        def test_method(src, cmp, state):
            return [(src, cmp)]

        self.assertIn("test", FILE_PAIRING_METHODS)

    def test_pair_by_file(self):
        expected = [(self.src, self.cmp)]
        result = pair_by_file(self.src, self.cmp)
        self.assertEqual(result, expected)

    def test_pair_by_line(self):
        expected = [("Hello", "Hello"), ("World", "Python")]
        result = pair_by_line(self.src, self.cmp)
        self.assertEqual(result, expected)

    def test_pair_by_line_comment(self):
        # This test assumes that the source and comparison files have comments on the
        # same lines
        # You may need to adjust this test based on your specific use case
        self.target = Path(__file__).parent / "target.py"
        self.reference = Path(__file__).parent / "reference.py"
        kwargs = {
            "token_limit": 100,
            "llm": None,
            "lang": "python",
            "target_file": self.target,
            "reference_file": self.reference,
        }
        expected = [("# Hello\n", "# Hello\n")]
        result = pair_by_line_comment(self.src, self.cmp, **kwargs)
        self.assertEqual(result, expected)
