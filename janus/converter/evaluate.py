from janus.converter.converter import Converter
from janus.language.combine import JsonCombiner
from janus.utils.logger import create_logger

# Parsers
from janus.parsers.eval_parsers.incose_parser import IncoseParser

log = create_logger(__name__)

class Evaluator(Converter):
    """Evaluator

    A class that performs an LLM self evaluation on an input target, with an associated prompt.

    Current valid evaluation types:
    ['incose']

    TODO:
    ['incose_set', 'comments', 'comments_set']
    """
    def __init__(
        self,
        evaluation_type, 
         **kwargs)->None:
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

        # Setting parser type
        if evaluation_type == "incose":
            self._parser = IncoseParser()
        else:
            raise ValueError("Parser not found. Please make sure the evaluation type is correct and the parser and prompt exsists.")
        
        self.set_prompt("eval_prompts/" + evaluation_type)