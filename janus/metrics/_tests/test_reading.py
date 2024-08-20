import unittest

from janus.metrics.reading import _repeat_text, flesch, gunning_fog


class TestReading(unittest.TestCase):
    def setUp(self):
        self.text = "This is a sample text for testing readability metrics"

    def test_repeat_text(self):
        """Test the _repeat_text function."""
        repeated_text = _repeat_text(self.text)
        self.assertIsInstance(repeated_text, str)
        self.assertTrue(len(repeated_text.split()) >= 100)

    def test_flesch(self):
        """Test the Flesch readability score."""
        score = flesch(self.text)
        self.assertAlmostEqual(score, 47.3, places=2)

    def test_gunning_fog(self):
        """Test the Gunning-Fog readability score."""
        score = gunning_fog(self.text)
        self.assertAlmostEqual(score, 8.04, places=2)


if __name__ == "__main__":
    unittest.main()
