import traceback
import unittest
from unittest.mock import ANY, patch

from typer.testing import CliRunner

from janus.cli import app, translate
from janus.embedding.embedding_models_info import EMBEDDING_MODEL_CONFIG_DIR
from janus.llm.models_info import MODEL_CONFIG_DIR


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

    def test_embedding_add(self):
        embedding_model_path = (
            EMBEDDING_MODEL_CONFIG_DIR / "test-embedding-model-name.json"
        )
        if embedding_model_path.exists():
            embedding_model_path.unlink()
        result = self.runner.invoke(
            app, ["embedding", "add", "test-embedding-model-name"]
        )
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(embedding_model_path.exists())
        embedding_model_path.unlink()

    def test_db_add_and_rm(self):
        embedding_model_path = (
            EMBEDDING_MODEL_CONFIG_DIR / "test-embedding-model-name.json"
        )
        if embedding_model_path.exists():
            embedding_model_path.unlink()
        result = self.runner.invoke(
            app,
            ["embedding", "add", "test-embedding-model-name", "-t", "HuggingFaceLocal"],
        )
        self.assertEqual(result.exit_code, 0)
        result = self.runner.invoke(
            app,
            [
                "db",
                "add",
                "test-db-name",
                "test-embedding-model-name",
                "-i",
                "janus/language/mumps",
            ],
        )
        traceback.print_exception(result.exception)
        embedding_model_path.unlink()
        self.assertEqual(result.exit_code, 0)

        result = self.runner.invoke(app, ["db", "rm", "test-db-name", "-y"])
        self.assertEqual(result.exit_code, 0)

    @patch("janus.converter.translate.Translator.translate", autospec=True)
    def test_translate(self, mock_translate):
        # Arrange
        mock_instance = mock_translate.return_value
        mock_instance.translate.return_value = None  # or whatever you expect

        # Act
        translate(
            source_lang="matlab",
            target_lang="python",
            input_dir="janus/",
            output_dir="janus/",
            overwrite=True,
            temp=0.7,
            prompt_template="simple",
            collection=None,
            llm_name="gpt-4o",
        )

        # Assert
        mock_translate.assert_called_once()
        mock_translate.assert_called_once_with(ANY, "janus/", "janus/", True, None)
