import unittest

from janus.metrics.reading import (
    _repeat_text,
    automated_readability,
    coleman_liau,
    dale_chall,
    flesch,
    flesch_grade,
    gunning_fog,
    word_count,
)


class TestReading(unittest.TestCase):
    def setUp(self):
        self.text = "This is a sample text for testing readability metrics."

    def test_word_count(self):
        """Test the word_count function."""
        count = word_count(self.text)
        self.assertEqual(count, 9)

    def test_repeat_text(self):
        """Test the _repeat_text function."""
        repeated_text = _repeat_text(self.text)
        self.assertIsInstance(repeated_text, str)
        self.assertTrue(len(repeated_text.split()) >= 100)

    def test_flesch(self):
        """Test the Flesch readability score."""
        score = flesch(self.text)
        self.assertAlmostEqual(score, 45.42, places=2)

    def test_flesch_grade(self):
        """Test the Flesch Grade Level readability score."""
        score = flesch_grade(self.text)
        self.assertAlmostEqual(score, 9.2, places=2)

    def test_gunning_fog(self):
        """Test the Gunning-Fog readability score."""
        score = gunning_fog(self.text)
        self.assertAlmostEqual(score, 3.97, places=2)

    def test_dale_chall(self):
        """Test the Dale-Chall readability score."""
        score = dale_chall(self.text)
        self.assertAlmostEqual(score, 4.67, places=2)

    def test_automated_readability(self):
        """Test the Automated Readability Index score."""
        score = automated_readability(self.text)
        self.assertAlmostEqual(score, 7.1, places=2)

    def test_coleman_liau(self):
        """Test the Coleman-Liau Index."""
        score = coleman_liau(self.text)
        self.assertAlmostEqual(score, 9.94, places=2)

    def test_blank_target(self):
        """Test that blank targets return None for all metric functions."""
        blank = "   "  # blank string with whitespaces
        self.assertIsNone(flesch(blank))
        self.assertIsNone(flesch_grade(blank))
        self.assertIsNone(gunning_fog(blank))
        self.assertIsNone(dale_chall(blank))
        self.assertIsNone(automated_readability(blank))
        self.assertIsNone(coleman_liau(blank))


if __name__ == "__main__":
    unittest.main()
