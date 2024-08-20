import logging
import os
import unittest
from unittest.mock import patch

from janus.utils.logger import LogFilter, create_logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.log_filter = LogFilter()
        self.record = logging.LogRecord(
            name="test", level=20, pathname="", lineno=0, msg="", args=(), exc_info=None
        )

    def test_log_filter(self):
        self.record.msg = "dealloc"
        self.assertFalse(self.log_filter.filter(self.record))

        self.record.msg = "That model is currently overloaded"
        self.assertFalse(self.log_filter.filter(self.record))

        self.record.msg = "Batches: "
        self.assertFalse(self.log_filter.filter(self.record))

        self.record.msg = "Using default tokenizer."
        self.assertFalse(self.log_filter.filter(self.record))

        self.record.msg = "Load pretrained SentenceTransformer"
        self.assertFalse(self.log_filter.filter(self.record))

        self.record.msg = "Use pytorch device"
        self.assertFalse(self.log_filter.filter(self.record))

        self.record.msg = "creating"
        self.assertFalse(self.log_filter.filter(self.record))

        self.record.msg = "cc -f"
        self.assertFalse(self.log_filter.filter(self.record))

        self.record.msg = "c++"
        self.assertFalse(self.log_filter.filter(self.record))

        self.record.msg = "error_code=context_length_exceeded"
        self.assertFalse(self.log_filter.filter(self.record))

        self.record.msg = "NumExpr"
        self.assertFalse(self.log_filter.filter(self.record))

        self.record.msg = "cc -shared"
        self.assertFalse(self.log_filter.filter(self.record))

        self.record.msg = "This is a test message"
        self.assertTrue(self.log_filter.filter(self.record))

    def test_create_logger(self):
        with patch.dict(os.environ, {"LOGLEVEL": "DEBUG"}):
            logger = create_logger("test")
            self.assertEqual(logger.level, logging.DEBUG)

        with patch.dict(os.environ, {}, clear=True):
            logger = create_logger("test")
            self.assertEqual(logger.level, logging.INFO)


if __name__ == "__main__":
    unittest.main()
