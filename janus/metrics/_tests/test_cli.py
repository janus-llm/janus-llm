# FILEPATH: /Users/mdoyle/projects/janus/janus/metrics/tests/test_cli.py

import unittest
from unittest.mock import mock_open, patch

from ..cli import evaluate_main, state


class TestEvaluateMain(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    @patch("janus.metrics.cli.load_model")
    @patch("janus.metrics.cli.FILE_PAIRING_METHODS")
    def test_evaluate_main(self, mock_methods, mock_load_model, mock_file):
        mock_load_model.return_value = ("llm", "token_limit", "model_cost")
        mock_methods.__getitem__.return_value = lambda src, cmp, state: "pairs"

        evaluate_main(
            "target_file",
            "reference_file",
            "out_file",
            "lang",
            "PAIR_BY_FILE",
            "gpt-3.5-turbo",
        )

        mock_file.assert_any_call("target_file", "r")
        mock_file.assert_any_call("reference_file", "r")
        mock_load_model.assert_called_once_with("gpt-3.5-turbo")
        mock_methods.__getitem__.assert_called_once_with("PAIR_BY_FILE")

        self.assertEqual(state["target_file"], "target_file")
        self.assertEqual(state["reference_file"], "reference_file")
        self.assertEqual(state["out_file"], "out_file")
        self.assertEqual(state["lang"], "lang")
        self.assertEqual(state["llm"], "llm")
        self.assertEqual(state["token_limit"], "token_limit")
        self.assertEqual(state["model_cost"], "model_cost")
        self.assertEqual(state["pairs"], "pairs")


if __name__ == "__main__":
    unittest.main()
