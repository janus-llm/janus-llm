import unittest

from typer.testing import CliRunner

from ..cli import app


class TestCli(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_help(self):
        result = self.runner.invoke(app, ["--help"])
        self.assertEqual(result.exit_code, 0)

    def test_version(self):
        result = self.runner.invoke(app, ["--version"])
        self.assertEqual(result.exit_code, 0)

    def test_invalid_command(self):
        result = self.runner.invoke(app, ["invalid_command"])
        self.assertNotEqual(result.exit_code, 0)

    def test_no_arguments(self):
        result = self.runner.invoke(app)
        self.assertEqual(result.exit_code, 0)
