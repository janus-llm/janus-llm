import unittest
from pathlib import Path

from typer.testing import CliRunner

from ...cli import app
from ..complexity_metrics import cyclomatic_complexity, effort


class TestTreesitterMetrics(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.target_text = """
                SAMP1    CSECT
                 STM   14,12,12(13)
                 BALR  12,0
                 USING *,12
                 ST    13,SAVE+4
                 LA    15,SAVE
                 ST    15,8(13)
                 LR    13,15
        STOP1    LH    3,HALFCON
        STOP2    A     3,FULLCON
        STOP3    ST    3,HEXCON
                 L     13,4(13)
                 LM    14,12,12(13)
                 BR    14
        SAVE     DC    18F'0'
        ADCON    DC    A(SAVE)
        FULLCON  DC    F'-1'
        HEXCON   DC    XL4'FD38'
        HALFCON  DC    H'32'
        CHARCON  DC    CL10'TEST EXAMP'
        PACKCON  DC    PL4'25'
        BINCON   DC    B'10101100'
                 END   SAMP1
         """

    def test_cyclomatic_complexity(self):
        """Test the cyclomatic complexity function."""
        function_score = cyclomatic_complexity(self.target_text, language="ibmhlasm")
        expected_score = 3
        self.assertEqual(function_score, expected_score)

    def test_halstead_effort(self):
        """Test the halstead effort."""
        function_score = effort(self.target_text, language="ibmhlasm")
        self.assertGreater(function_score, 0)

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
