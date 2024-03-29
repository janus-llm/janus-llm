import unittest

from ..cyclomatic_complexity import cyclomatic_complexity


class TestCyclomaticComplexity(unittest.TestCase):
    def setUp(self):
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
        """Test the cyclomayfunction with custom parameters."""
        function_score = cyclomatic_complexity(self.target_text, language="ibmhlasm")
        expected_score = 2
        self.assertEqual(function_score, expected_score)


if __name__ == "__main__":
    unittest.main()
