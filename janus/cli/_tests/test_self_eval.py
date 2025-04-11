import unittest

from typer.testing import CliRunner

from janus.cli.cli import app


class Testllm_self_eval(unittest.TestCase):
    """Tests for the DiagramGenerator class."""

    def setUp(self):
        """Set up the tests."""
        self.runner = CliRunner()

    def test_self_eval_cli(self):
        """Test self-eval cli method."""

        result = self.runner.invoke(app, ["llm-self-eval", "-h"])
        self.assertEqual(result.exit_code, 0)
