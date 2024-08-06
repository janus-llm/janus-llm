import unittest

from sacrebleu import sentence_chrf

from janus.metrics.chrf import chrf


class TestChrF(unittest.TestCase):
    def setUp(self):
        self.target_text = "This is a source text."
        self.reference_text = "This is a destination text."
        self.char_order = 6
        self.word_order = 2
        self.beta = 2.0

    def test_chrf_custom_params(self):
        """Test the chrf function with custom parameters."""
        function_score = chrf(
            self.target_text,
            self.reference_text,
            self.char_order,
            self.word_order,
            self.beta,
        )
        score = sentence_chrf(
            hypothesis=self.target_text,
            references=[self.reference_text],
            char_order=self.char_order,
            word_order=self.word_order,
            beta=self.beta,
        )
        expected_score = float(score.score) / 100.0
        self.assertEqual(function_score, expected_score)

    def test_chrf_with_s_flag(self):
        """Test the CHRF score calculation with the -S flag."""
        function_score = sentence_chrf(
            hypothesis=self.target_text,
            references=[self.reference_text],
            char_order=self.char_order,
            word_order=self.word_order,
            beta=self.beta,
        )
        function_score = float(function_score.score) / 100.0
        score_with_s_flag = chrf(
            self.target_text,
            self.reference_text,
            self.char_order,
            self.word_order,
            self.beta,
            use_strings=True,  # Mimics -S
        )
        self.assertEqual(function_score, score_with_s_flag)

    def test_chrf_invalid_target_type(self):
        """Test the chrf function with invalid source text type."""
        with self.assertRaises(TypeError):
            chrf(123, self.reference_text, self.char_order, self.word_order, self.beta)

    def test_chrf_invalid_reference_type(self):
        """Test the chrf function with invalid destination text type."""
        with self.assertRaises(TypeError):
            chrf(self.target_text, 123, self.char_order, self.word_order, self.beta)


if __name__ == "__main__":
    unittest.main()
