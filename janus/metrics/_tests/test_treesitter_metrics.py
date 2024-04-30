import unittest
from pathlib import Path

from typer.testing import CliRunner

from ...cli import app
from ..complexity_metrics import (
    TreeSitterMetric,
    cyclomatic_complexity,
    difficulty,
    effort,
    maintainability,
    volume,
)


class TestTreesitterMetrics(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        file = Path(__file__).parent.resolve() / "asm_test_file.asm"
        self.target_text = file.read_text()

    def test_cyclomatic_complexity(self):
        """Test the cyclomatic complexity function."""
        function_score = cyclomatic_complexity(self.target_text, language="ibmhlasm")
        expected_score = 3
        self.assertEqual(function_score, expected_score)

    def test_length(self):
        """Test the get_program_vocabulary function."""
        tsm = TreeSitterMetric(code=self.target_text, language="ibmhlasm")
        function_score = tsm.get_program_length()
        expected_score = 18
        self.assertEqual(function_score, expected_score)

    def test_vocabulary(self):
        """Test the get_program_vocabulary function."""
        tsm = TreeSitterMetric(code=self.target_text, language="ibmhlasm")
        function_score = tsm.get_program_vocabulary()
        expected_score = 9
        self.assertEqual(function_score, expected_score)

    def test_difficulty(self):
        """Test the get_program_vocabulary function."""
        function_score = difficulty(self.target_text, language="ibmhlasm")
        expected_score = 5
        self.assertEqual(function_score, expected_score)

    def test_effort(self):
        """Test the halstead effort."""
        function_score = effort(self.target_text, language="ibmhlasm")
        self.assertAlmostEqual(function_score, 285.29, places=2)

    def test_volume(self):
        """Test the halstead volume."""
        function_score = volume(self.target_text, language="ibmhlasm")
        self.assertAlmostEqual(function_score, 57.06, places=2)

    def test_maintainability(self):
        """Test the halstead volume."""
        function_score = maintainability(self.target_text, language="ibmhlasm")
        self.assertAlmostEqual(function_score, 65.48, places=2)

    def test_in_cli(self):
        """Test the function in the CLI."""
        output_path = Path("test.json")
        if output_path.exists():
            output_path.unlink()
        result = self.runner.invoke(
            app,
            [
                "evaluate",
                "cyclomatic-complexity",
                "-l",
                "ibmhlasm",
                "-t",
                "janus/language/treesitter/_tests/languages/ibmhlasm.asm",
                "-o",
                f"{output_path}",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(output_path.exists())
        output_path.unlink()


if __name__ == "__main__":
    unittest.main()
