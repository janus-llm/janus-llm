import unittest

from janus.metrics.similarity import similarity_score


class TestSimilarityScore(unittest.TestCase):
    def setUp(self):
        self.target = "This is a test sentence."
        self.reference = "This is a reference sentence."

    def test_similarity_score(self):
        score = similarity_score(self.target, self.reference)
        self.assertIsInstance(score, float)
