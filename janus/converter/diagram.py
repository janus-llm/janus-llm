from langchain_core.runnables import Runnable, RunnableParallel

from janus.converter.document import Documenter
from janus.converter.merge import MergedOutputConverterMixin
from janus.parsers.uml import UMLSyntaxParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class DiagramGenerator(Documenter):
    """A Converter that translates code into a set of PLANTUML diagrams."""

    def __init__(
        self,
        prompt_template: str = "diagram",
        diagram_type: str = "Activity",
        output_type: str = "diagram",
        **kwargs,
    ) -> None:
        """Initialize the DiagramGenerator class

        Arguments:
            diagram_type: type of PLANTUML diagram to generate
            add_documentation: Whether to add a documentation step prior to
                diagram generation.
        """
        super().__init__(
            prompt_template=prompt_template,
            output_type=output_type,
            **kwargs,
        )

        self._parser = UMLSyntaxParser(language="plantuml")
        self._diagram_type = diagram_type

    def _input_runnable(self) -> Runnable:
        return RunnableParallel(
            SOURCE_CODE=self._parser.parse_input,
            context=self._retriever,
            DIAGRAM_TYPE=lambda x: self._diagram_type,
        )


class MergedOutputDiagramGenerator(MergedOutputConverterMixin, DiagramGenerator):
    """A class that translates outputs from the OutputMerger to code."""

    def __init__(
        self,
        prompt_template: str = "diagram_with_documentation",
        input_labels: set[str] | str | None = None,
        target_language: str = "python",
        **kwargs,
    ) -> None:
        if input_labels is None:
            raise ValueError("MergedOutputDiagramGenerator requires input labels")
        super().__init__(
            input_labels=input_labels,
            target_language=target_language,
            prompt_template=prompt_template,
            **kwargs,
        )

    def _input_runnable(self) -> Runnable:
        runnable = super()._input_runnable()
        return runnable.assign(
            DIAGRAM_TYPE=lambda x: self._diagram_type,
        )
