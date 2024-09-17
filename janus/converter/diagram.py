import math

from langchain.output_parsers import RetryWithErrorOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.runnables import RunnableLambda, RunnableParallel

from janus.converter.converter import run_if_changed
from janus.converter.document import Documenter
from janus.language.block import TranslatedCodeBlock
from janus.llm.models_info import MODEL_PROMPT_ENGINES
from janus.parsers.refiner_parser import RefinerParser
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

    def _run_chain(self, block: TranslatedCodeBlock) -> str:
        input = self._parser.parse_input(block.original)
        n1 = round(self.max_prompts ** (1 / 3))

        # Retries with the input, output, and error
        n2 = round((self.max_prompts // n1) ** (1 / 2))

        # Retries with just the input
        n3 = math.ceil(self.max_prompts / (n1 * n2))

        if self._add_documentation:
            documentation_text = super()._run_chain(block)
            refine_output = RefinerParser(
                parser=self._diagram_parser,
                initial_prompt=self._diagram_prompt.format(
                    **{
                        "SOURCE_CODE": input,
                        "DOCUMENTATION": documentation_text,
                        "DIAGRAM_TYPE": self._diagram_type,
                    }
                ),
                refiner=self._refiner,
                max_retries=n1,
                llm=self._llm,
            )
        else:
            refine_output = RefinerParser(
                parser=self._diagram_parser,
                initial_prompt=self._diagram_prompt.format(
                    **{
                        "SOURCE_CODE": input,
                        "DIAGRAM_TYPE": self._diagram_type,
                    }
                ),
                refiner=self._refiner,
                max_retries=n1,
                llm=self._llm,
            )
        retry = RetryWithErrorOutputParser.from_llm(
            llm=self._llm,
            parser=refine_output,
            max_retries=n2,
        )
        completion_chain = self._prompt | self._llm
        chain = RunnableParallel(
            completion=completion_chain, prompt_value=self._diagram_prompt
        ) | RunnableLambda(lambda x: retry.parse_with_prompt(**x))
        for _ in range(n3):
            try:
                if self._add_documentation:
                    return chain.invoke(
                        {
                            "SOURCE_CODE": input,
                            "DOCUMENTATION": documentation_text,
                            "DIAGRAM_TYPE": self._diagram_type,
                        }
                    )
                else:
                    return chain.invoke(
                        {
                            "SOURCE_CODE": input,
                            "DIAGRAM_TYPE": self._diagram_type,
                        }
                    )
            except OutputParserException:
                pass

        raise OutputParserException(f"Failed to parse after {n1*n2*n3} retries")

    @run_if_changed(
        "_diagram_prompt_template_name",
        "_source_language",
    )
    def _load_diagram_prompt_engine(self) -> None:
        """Load the prompt engine according to this instance's attributes.

        If the relevant fields have not been changed since the last time this method was
        called, nothing happens.
        """
        self._diagram_prompt_engine = MODEL_PROMPT_ENGINES[self._model_id](
            source_language=self._source_language,
            target_language="text",
            target_version=None,
            prompt_template=self._diagram_prompt_template_name,
        )
        self._diagram_prompt = self._diagram_prompt_engine.prompt
