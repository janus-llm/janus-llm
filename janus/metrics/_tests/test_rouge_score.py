import unittest

from janus.metrics.rouge_score import rouge


class TestRouge(unittest.TestCase):
    def setUp(self):
        self.target = "This is a test sentence."
        self.reference = "This is a reference sentence."

    def test_rouge_with_granularity_n(self):
        score = rouge(
            self.target, self.reference, granularity="n", n_gram=2, score_type="f"
        )
        self.assertIsInstance(score, float)

    def test_rouge_with_granularity_l(self):
        score = rouge(
            self.target, self.reference, granularity="l", n_gram=2, score_type="f"
        )
        self.assertIsInstance(score, float)

    def test_rouge_with_granularity_w(self):
        score = rouge(
            self.target, self.reference, granularity="w", n_gram=2, score_type="f"
        )
        self.assertIsInstance(score, float)

    def test_rouge_with_invalid_granularity(self):
        with self.assertRaises(ValueError):
            rouge(
                self.target,
                self.reference,
                granularity="invalid",
                n_gram=2,
                score_type="f",
            )

    def test_rouge_with_score_type_f(self):
        score = rouge(
            self.target, self.reference, granularity="n", n_gram=2, score_type="f"
        )
        self.assertIsInstance(score, float)

    def test_rouge_with_score_type_p(self):
        score = rouge(
            self.target, self.reference, granularity="n", n_gram=2, score_type="p"
        )
        self.assertIsInstance(score, float)

    def test_rouge_with_score_type_r(self):
        score = rouge(
            self.target, self.reference, granularity="n", n_gram=2, score_type="r"
        )
        self.assertIsInstance(score, float)

    def test_rouge_with_invalid_score_type(self):
        with self.assertRaises(ValueError):
            rouge(
                self.target,
                self.reference,
                granularity="n",
                n_gram=2,
                score_type="invalid",
            )
