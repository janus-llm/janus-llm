from janus.converter.converter import Converter
from janus.language.combine import JsonCombiner
from janus.utils.logger import create_logger

log = create_logger(__name__)


class Evaluator(Converter):
    """Evaluator

    A class that performs an LLM self evaluation"
    "on an input target, with an associated prompt.

    Current valid evaluation types:
    ['incose', 'comments', 'inline_comments']

    TODO:
    ['incose_set']
    """

    def __init__(self, **kwargs) -> None:
        """Initialize the Evaluator class

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set and the
                `OPENAI_ORG_ID` environment variable should be set if needed.
            model_arguments: Additional arguments to pass to the LLM constructor.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        super().__init__(**kwargs)
        self._combiner = JsonCombiner()
        self._load_parameters()
