from langchain_core.runnables import Runnable, RunnableParallel

from janus.converter.document import Documenter
from janus.parsers.uml import UMLSyntaxParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class DiagramGenerator(Documenter):
    """A Converter that translates code into a set of PLANTUML diagrams."""

    def __init__(
        self,
        diagram_type="Activity",
        add_documentation=False,
        **kwargs,
    ) -> None:
        """Initialize the DiagramGenerator class

        Arguments:
            diagram_type: type of PLANTUML diagram to generate
            add_documentation: Whether to add a documentation step prior to
                diagram generation.
        """
        self._diagram_type = diagram_type
        self._add_documentation = add_documentation
        self._documenter = Documenter(**kwargs)

        super().__init__(**kwargs)

        self.set_prompt("diagram_with_documentation" if add_documentation else "diagram")
        self._parser = UMLSyntaxParser(language="plantuml")

        self._load_parameters()

    def _load_prompt(self):
        super()._load_prompt()
        self._prompt = self._prompt.partial(DIAGRAM_TYPE=self._diagram_type)

    def _input_runnable(self) -> Runnable:
        if self._add_documentation:
            return RunnableParallel(
                SOURCE_CODE=self._parser.parse_input,
                DOCUMENTATION=self._documenter.chain,
                context=self._retriever,
            )
        return RunnableParallel(
            SOURCE_CODE=self._parser.parse_input,
            context=self._retriever,
        )
