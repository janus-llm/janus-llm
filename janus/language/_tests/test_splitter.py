import unittest

from janus.language.splitter import Splitter


class TestSplitter(unittest.TestCase):
    def setUp(self):
        self.splitter = Splitter(language="python")

    def test_split(self):
        input_data = "janus/__main__.py"
        self.assertRaises(NotImplementedError, self.splitter.split, input_data)


if __name__ == "__main__":
    unittest.main()
