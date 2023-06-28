"""Any Python-specific combination functionality should be defined here.
"""
from ..combine import Combiner


class PythonCombiner(Combiner):
    """A class that combines code blocks into Python files."""

    def __init__(self) -> None:
        """Initialize a PythonCombiner instance."""
        super().__init__("python")
