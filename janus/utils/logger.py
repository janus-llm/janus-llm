import logging
import os

from rich.logging import RichHandler


class LogFilter(logging.Filter):
    """
    Print all messages that do not include "dealloc" (GPU warning message).
    """

    def filter(self, record: logging.LogRecord):
        # This is a `numba` warning that is not useful to print
        # Probably wouldn't come up in this project, but keeping it in here as an example
        if "dealloc" in str(getattr(record, "msg")):
            return False
        elif "That model is currently overloaded" in str(getattr(record, "msg")):
            return False
        elif "Batches: " in str(getattr(record, "msg")):
            return False
        elif "Using default tokenizer." in str(getattr(record, "msg")):
            return False
        elif "Load pretrained SentenceTransformer" in str(getattr(record, "msg")):
            return False
        elif "Use pytorch device" in str(getattr(record, "msg")):
            return False
        elif "creating" in str(getattr(record, "msg")):
            return False
        elif "cc -f" in str(getattr(record, "msg")):
            return False
        elif "c++" in str(getattr(record, "msg")):
            return False
        elif "error_code=context_length_exceeded" in str(getattr(record, "msg")):
            return False
        elif "NumExpr" in str(getattr(record, "msg")):
            return False
        elif "cc -shared" in str(getattr(record, "msg")):
            return False
        return True

    def __repr__(self):
        return "LogFilter"


def create_logger(name: str) -> logging.Logger:
    """Create a `Logger` to be used in different modules

    Parameters:
    -----------
    name: str
        The name of the logger. Will usually be passed in from the module as `__name__`.

    Returns:
    --------
    log: logging.Logger
        The `Logger` object that will be used to create log statements in the terminal.
    """
    if (log_level := os.environ.get("LOGLEVEL")) is None:
        log_level = "INFO"

    FORMAT = "%(message)s"
    rh = RichHandler()
    rh.addFilter(LogFilter())
    handlers = [rh]
    logging.basicConfig(
        level=log_level,
        format=FORMAT,
        datefmt="[%m/%d/%Y %I:%M:%S %p]",
        handlers=handlers,
    )

    log = logging.getLogger(name)
    log.setLevel(log_level)

    return log
