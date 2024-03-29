import unittest

from janus.metrics.rouge_score import rouge


class TestRouge(unittest.TestCase):
    def setUp(self):
        self.target = "This is a test sentence."
        self.reference = "This is a reference sentence."

    def test_rouge_with_integer_ngram(self):
        score = rouge(self.target, self.reference, n_gram=2)
        self.assertIsInstance(score, float)

    def test_rouge_with_l_ngram(self):
        score = rouge(self.target, self.reference, n_gram="L")
        self.assertIsInstance(score, float)

    def test_rouge_with_invalid_ngram(self):
        with self.assertRaises(ValueError):
            rouge(self.target, self.reference, n_gram="invalid")

    def test_rouge_with_same_target_and_reference(self):
        score = rouge(self.target, self.target, n_gram=2)
        self.assertEqual(score, 1.0)


if __name__ == "__main__":
    unittest.main()
