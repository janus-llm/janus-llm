import unittest
from unittest.mock import patch

import pytest

from janus.llm.models_info import load_model
from janus.metrics.llm_metrics import llm_evaluate_option, llm_evaluate_ref_option


class TestLLMMetrics(unittest.TestCase):
    def setUp(self):
        self.bad_code = """
        if __name__ == "__main__":
            a1, a2, b3, b4 = 0, [1, 2000, "a"], 2, (1, 2)
        for a in a2:
            if b3:
            elif not b3:
                try:
                    pass
                except:
                    raise ValueError
            elif 1:
                print(1)
            else:
                print(b4[0])
                for (x, y) in range(a1, b3):
                    for i in range(003300):
                        for z in a2:
                            printf(b4[2])
        """
        self.impressive_code = """
        # This program prints out Hello, world!

        print('Hello, world!')
        """
        self.impressive_code_reference = """
        # An implementation of python Hello, world!

        print("'Hello, world!")
        """

    @patch(".llm.models_info.load_model")
    @patch("janus.metrics.llm_metrics.llm_evaluate")
    @pytest.mark.llm_eval
    def test_llm_self_eval_quality(self, mock_llm_evaluate, mock_load_model):
        """Test that the quality llm self eval recognizes bad_code as bad code
        (<5 on a scale of 1-10)"""
        mock_llm_evaluate.return_value = 4  # return a value less than 5
        mock_load_model.return_value = [None]  # return a dummy model

        bad_code_quality = llm_evaluate_option(
            self.bad_code,
            self.bad_code,
            metric="quality",
            language="python",
            llm=load_model("gpt-4o")[0],
        )
        self.assertLess(bad_code_quality, 5)

        mock_llm_evaluate.return_value = 6  # return a value greater than 5
        impressive_code_quality = llm_evaluate_option(
            self.impressive_code,
            self.impressive_code,
            metric="quality",
            language="python",
            llm=load_model("gpt-4o")[0],
        )
        self.assertGreater(impressive_code_quality, 5)

    @patch("janus.llm.models_info.load_model")
    @patch("janus.metrics.llm_metrics.llm_evaluate")
    @pytest.mark.llm_eval
    def test_llm_self_eval_faithfulness(self, mock_llm_evaluate, mock_load_model):
        """The two Hello, world! samples are more or less the same,
        so the faithfulness score should be high"""
        mock_llm_evaluate.return_value = 9  # return a high value
        mock_load_model.return_value = [None]  # return a dummy model

        faithfulness = llm_evaluate_ref_option(
            self.impressive_code,
            self.impressive_code_reference,
            metric="faithfulness",
            language="python",
            llm=load_model("gpt-4o")[0],
        )
        self.assertGreater(faithfulness, 8)


if __name__ == "__main__":
    unittest.main()
