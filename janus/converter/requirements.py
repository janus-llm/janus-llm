from janus.converter.document import Documenter
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
        super().__init__(output_type=output_type, combine_output=combine_output, **kwargs)
        self._prompt_template_names = ["requirements"]
        self._parser = RequirementsParser()
