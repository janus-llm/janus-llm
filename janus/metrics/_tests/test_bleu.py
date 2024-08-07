import unittest

from sacrebleu import sentence_bleu

from janus.metrics.bleu import bleu


class TestBLEU(unittest.TestCase):
    def setUp(self):
        self.target_text = "This is a source text."
        self.reference_text = "This is a destination text."

    def test_bleu(self):
        """Test the BLEU score calculation."""
        function_score = (
            sentence_bleu(
                self.target_text,
                [self.reference_text],
            ).score
            / 100.0
        )
        expected_score = bleu(
            self.target_text,
            self.reference_text,
        )
        self.assertEqual(function_score, expected_score)

    def test_bleu_with_s_flag(self):
        """Test the BLEU score calculation with the -S flag."""
        function_score = (
            sentence_bleu(
                self.target_text,
                [self.reference_text],
            ).score
            / 100.0
        )
        score_with_s_flag = bleu(
            self.target_text,
            self.reference_text,
            use_strings=True,  # Mimics -S
        )
        self.assertEqual(function_score, score_with_s_flag)

    def test_bleu_invalid_target_type(self):
        """Test the BLEU score calculation with invalid source text type."""
        with self.assertRaises(TypeError):
            sentence_bleu(123, [self.reference_text])

    def test_bleu_invalid_reference_type(self):
        """Test the BLEU score calculation with invalid destination text type."""
        with self.assertRaises(TypeError):
            sentence_bleu(self.target_text, 123)


if __name__ == "__main__":
    unittest.main()
