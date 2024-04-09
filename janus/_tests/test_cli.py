import unittest

from typer.testing import CliRunner

from ..cli import app
from ..llm.models_info import MODEL_CONFIG_DIR


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

    def test_translate_help(self):
        result = self.runner.invoke(app, ["translate", "-h"])
        self.assertEqual(result.exit_code, 0)

    def test_document_help(self):
        result = self.runner.invoke(app, ["document", "-h"])
        self.assertEqual(result.exit_code, 0)

    def test_db_help(self):
        result = self.runner.invoke(app, ["db", "-h"])
        self.assertEqual(result.exit_code, 0)

    def test_llm_help(self):
        result = self.runner.invoke(app, ["llm", "-h"])
        self.assertEqual(result.exit_code, 0)

    def test_llm_add(self):
        llm_model_path = MODEL_CONFIG_DIR / "test-model-name.json"
        if llm_model_path.exists():
            llm_model_path.unlink()
        result = self.runner.invoke(app, ["llm", "add", "test-model-name"])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(llm_model_path.exists())
        llm_model_path.unlink()

    def test_db_ls(self):
        result = self.runner.invoke(app, ["db", "ls"])
        self.assertEqual(result.exit_code, 0)

    def test_db_status(self):
        result = self.runner.invoke(app, ["db", "status"])
        self.assertEqual(result.exit_code, 0)

    def test_db_add_and_rm(self):
        result = self.runner.invoke(app, ["db", "add", "test-db-name"])
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(app, ["db", "rm", "test-db-name", "-y"])
        self.assertEqual(result.exit_code, 0)
