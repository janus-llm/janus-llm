from ..utils.enums import LANGUAGES
from ..utils.logger import create_logger

log = create_logger(__name__)


class FileManager:
    """A parent class that manages the files that are being translated."""

    def __init__(self, language: str = "python") -> None:
        self.language: str = language
        self.comment: str = LANGUAGES[self.language]["comment"]
        self.suffix: str = LANGUAGES[self.language]["suffix"]
