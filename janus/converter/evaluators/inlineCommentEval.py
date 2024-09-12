from janus.converter.evaluate import Evaluator
from janus.language.combine import JsonCombiner
from janus.parsers.eval_parsers.inline_comment_parser import InlineCommentParser

from janus.utils.logger import create_logger

log = create_logger(__name__)


class InlineCommentEvaluator(Evaluator):
    """Comment Evaluator

    A class that performs an LLM self evaluation on inline comments,
    with an associated prompt.
    """

    def __init__(
        self, evaluation_type, **kwargs
    ) -> None:
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
        print("Evaluating for: ", evaluation_type)
        self._parser = InlineCommentParser()
        self.set_prompt("eval_prompts/inline_comments")
