import unittest
from pathlib import Path

from typer.testing import CliRunner

from janus.cli import app
from janus.metrics.complexity_metrics import (
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
        asm_file = Path(__file__).parent.resolve() / "asm_test_file.asm"
        self.asm_target_text = asm_file.read_text()
        mumps_file = Path(__file__).parent.resolve() / "mumps_test_file.m"
        self.mumps_target_text = mumps_file.read_text()

    def test_cyclomatic_complexity(self):
        """Test the cyclomatic complexity function."""
        function_score = cyclomatic_complexity(self.asm_target_text, language="ibmhlasm")
        expected_score = 3
        self.assertEqual(function_score, expected_score)
        function_score = cyclomatic_complexity(self.mumps_target_text, language="mumps")
        expected_score = 2
        self.assertEqual(function_score, expected_score)

    def test_length(self):
        """Test the get_program_vocabulary function."""
        tsm_asm = TreeSitterMetric(code=self.asm_target_text, language="ibmhlasm")
        function_score = tsm_asm.get_program_length()
        expected_score = 18
        self.assertEqual(function_score, expected_score)
        tsm_mumps = TreeSitterMetric(code=self.mumps_target_text, language="mumps")
        function_score = tsm_mumps.get_program_length()
        expected_score = 11
        self.assertEqual(function_score, expected_score)

    def test_vocabulary(self):
        """Test the get_program_vocabulary function."""
        tsm_asm = TreeSitterMetric(code=self.asm_target_text, language="ibmhlasm")
        function_score = tsm_asm.get_program_vocabulary()
        expected_score = 9
        self.assertEqual(function_score, expected_score)
        tsm_mumps = TreeSitterMetric(code=self.mumps_target_text, language="mumps")
        function_score = tsm_mumps.get_program_vocabulary()
        expected_score = 7
        self.assertEqual(function_score, expected_score)

    def test_difficulty(self):
        """Test the get_program_vocabulary function."""
        function_score = difficulty(self.asm_target_text, language="ibmhlasm")
        expected_score = 5
        self.assertEqual(function_score, expected_score)
        function_score = difficulty(self.mumps_target_text, language="mumps")
        expected_score = 2.625
        self.assertAlmostEqual(function_score, expected_score, places=2)

    def test_effort(self):
        """Test the halstead effort."""
        function_score = effort(self.asm_target_text, language="ibmhlasm")
        self.assertAlmostEqual(function_score, 285.29, places=2)
        function_score = effort(self.mumps_target_text, language="mumps")
        self.assertAlmostEqual(function_score, 81.06, places=2)

    def test_volume(self):
        """Test the halstead volume."""
        function_score = volume(self.asm_target_text, language="ibmhlasm")
        self.assertAlmostEqual(function_score, 57.06, places=2)
        function_score = volume(self.mumps_target_text, language="mumps")
        self.assertAlmostEqual(function_score, 30.88, places=2)

    def test_maintainability(self):
        """Test the halstead volume."""
        function_score = maintainability(self.asm_target_text, language="ibmhlasm")
        self.assertAlmostEqual(function_score, 65.48, places=2)
        function_score = maintainability(self.mumps_target_text, language="mumps")
        self.assertAlmostEqual(function_score, 72.326, places=2)

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
