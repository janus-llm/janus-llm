import json
from copy import deepcopy

from janus.converter.converter import run_if_changed
from janus.converter.document import Documenter
from janus.language.block import TranslatedCodeBlock
from janus.llm.models_info import MODEL_PROMPT_ENGINES
from janus.parsers.uml import UMLSyntaxParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class DiagramGenerator(Documenter):
    """DiagramGenerator

    A class that translates code from one programming language to a set of diagrams.
    """

    def __init__(
        self,
        diagram_type="Activity",
        add_documentation=False,
        **kwargs,
    ) -> None:
        """Initialize the DiagramGenerator class

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set and the
                `OPENAI_ORG_ID` environment variable should be set if needed.
            model_arguments: Additional arguments to pass to the LLM constructor.
            source_language: The source programming language.
            max_prompts: The maximum number of prompts to try before giving up.
            db_path: path to chroma database
            db_config: database configuraiton
            diagram_type: type of PLANTUML diagram to generate
        """
        super().__init__(**kwargs)
        self._diagram_type = diagram_type
        self._add_documentation = add_documentation
        self._documenter = None
        self._diagram_parser = UMLSyntaxParser(language="plantuml")
        if add_documentation:
            self._diagram_prompt_template_name = "diagram_with_documentation"
        else:
            self._diagram_prompt_template_name = "diagram"
        self._load_diagram_prompt_engine()

    def _add_translation(self, block: TranslatedCodeBlock) -> None:
        """Given an "empty" `TranslatedCodeBlock`, translate the code represented in
        `block.original`, setting the relevant fields in the translated block. The
        `TranslatedCodeBlock` is updated in-pace, nothing is returned. Note that this
        translates *only* the code for this block, not its children.

        Arguments:
            block: An empty `TranslatedCodeBlock`
        """
        if block.translated:
            return

        if block.original.text is None:
            block.translated = True
            return

        if self._add_documentation:
            documentation_block = deepcopy(block)
            super()._add_translation(documentation_block)
            if not documentation_block.translated:
                message = "Error: unable to produce documentation for code block"
                log.info(message)
                raise ValueError(message)
            documentation = json.loads(documentation_block.text)["docstring"]

        if self._llm is None:
            message = (
                "Model not configured correctly, cannot translate. Try setting "
                "the model"
            )
            log.error(message)
            raise ValueError(message)

        log.debug(f"[{block.name}] Translating...")
        log.debug(f"[{block.name}] Input text:\n{block.original.text}")

        self._parser.set_reference(block.original)

        query_and_parse = self.diagram_prompt | self._llm | self._diagram_parser

        if self._add_documentation:
            block.text = query_and_parse.invoke(
                {
                    "SOURCE_CODE": block.original.text,
                    "DIAGRAM_TYPE": self._diagram_type,
                    "DOCUMENTATION": documentation,
                }
            )
        else:
            block.text = query_and_parse.invoke(
                {
                    "SOURCE_CODE": block.original.text,
                    "DIAGRAM_TYPE": self._diagram_type,
                }
            )
        block.tokens = self._llm.get_num_tokens(block.text)
        block.translated = True

        log.debug(f"[{block.name}] Output code:\n{block.text}")

    @run_if_changed(
        "_diagram_prompt_template_name",
        "_source_language",
    )
    def _load_diagram_prompt_engine(self) -> None:
        """Load the prompt engine according to this instance's attributes.

        If the relevant fields have not been changed since the last time this method was
        called, nothing happens.
        """
        self._diagram_prompt_engine = MODEL_PROMPT_ENGINES[self._model_name](
            source_language=self._source_language,
            target_language="text",
            target_version=None,
            prompt_template=self._diagram_prompt_template_name,
        )
        self.diagram_prompt = self._diagram_prompt_engine.prompt
