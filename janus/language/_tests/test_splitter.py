import unittest

from janus.language.splitter import Splitter


class TestSplitter(unittest.TestCase):
    def setUp(self):
        self.splitter = Splitter(language="python")

    def test_split(self):
        self.assertRaises(FileNotFoundError, self.splitter.split, "not-a-real-file.py")
        self.assertRaises(NotImplementedError, self.splitter.split, __file__)


if __name__ == "__main__":
    unittest.main()
