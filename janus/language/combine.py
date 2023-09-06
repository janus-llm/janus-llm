from .file import FileManager


class Combiner(FileManager):
    """No special functionality for the Combiner class yet."""

    def __init__(self, language: str = "python") -> None:
        """Initialize a Combiner instance.

        Arguments:
            language: The name of the language to combine.
        """
        super().__init__(language)
