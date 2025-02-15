from janus.converter.document import Documenter
from janus.language.combine import ChunkCombiner
from janus.parsers.reqs_parser import RequirementsParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class RequirementsDocumenter(Documenter):
    """RequirementsGenerator

    A class that translates code from one programming language to its requirements.
    """

    def __init__(
        self, combine_output: bool = False, output_type: str = "requirements", **kwargs
    ):
        kwargs.update(output_type=output_type)
        super().__init__(combine_output=combine_output, **kwargs)
        self.set_prompts("requirements")
        self._combiner = ChunkCombiner()
        self._parser = RequirementsParser()
        self._load_parameters()
