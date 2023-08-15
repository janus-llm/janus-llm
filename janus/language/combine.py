from .file import FileManager


class Combiner(FileManager):
    """ """

    def __init__(self, language: str = "python") -> None:
        """ """
        super().__init__(language)


class TextCombiner(Combiner):
    """A class that combines code blocks into text files."""

    def __init__(self) -> None:
        """Initialize a MumpsCombiner instance."""
        super().__init__("text")
