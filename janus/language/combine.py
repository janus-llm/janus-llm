from .file import FileManager
from ..utils.logger import create_logger
from .block import CodeBlock

log = create_logger(__name__)


class Combiner(FileManager):
    """No special functionality for the Combiner class yet."""

    def __init__(self, language: str = "python") -> None:
        """Initialize a Combiner instance.

        Arguments:
            language: The name of the language to combine.
        """
        super().__init__(language)

    def validate(self, code: str, input_block: CodeBlock) -> bool:
        for child in input_block.children:
            placeholder = f"{self.comment} {child.id}"
            if placeholder not in code:
                log.warning(f"Child placeholder ({child.id}) not present in code")
                log.debug(f"Code:\n{code}")
                return False
        return True
