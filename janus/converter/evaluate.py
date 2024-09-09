import json
from copy import deepcopy

from janus.converter.converter import Converter
from janus.language.combine import JsonCombiner
from janus.utils.logger import create_logger
from janus.language.block import TranslatedCodeBlock

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
        eval_items_per_request: int | None = None,
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
        self.eval_items_per_request = eval_items_per_request

        # Setting parser type here
        if evaluation_type == "incose":
            self._parser = IncoseParser()

        else:
            raise ValueError("Parser not found. Please make sure the evaluation type is correct and the parser and prompt exsists.")
        
        self.set_prompt("eval_prompts/" + evaluation_type)

    def _add_translation(self, block: TranslatedCodeBlock):
        if block.translated:
            return

        if block.original.text is None:
            block.translated = True
            return

        if self.eval_items_per_request is None:
            return super()._add_translation(block)
             
        temp = json.loads(block.original.text)
        # TODO: will need to dynamically update this so that if the object is changed in the input it will find the correct "thing"
        eval_item_type = "requirements"
        items = temp.get(eval_item_type, [])

        if not items:
            log.info(f"[{block.name}] Skipping commentless block")
            block.translated = True
            block.text = None
            block.complete = True
            return

        if len(items) <= self.eval_items_per_request:
            return super()._add_translation(block)

        # split the array into processable chunks. 
        chunk_size = self.eval_items_per_request
        # chunks is the split up version of them 
        chunks = []
        for i in range(0, len(items), chunk_size):
            chunk = items[i:i + chunk_size]
            chunks.append(chunk)

        block.processing_time = 0
        block.cost = 0
        block.retries = 0
        obj = {}
        for chunk in chunks:
            # Build a new TranslatedBlock using the new working text
            working_copy = deepcopy(block.original)
            working_copy.text = str(chunk)
            working_block = TranslatedCodeBlock(working_copy, self._target_language)

            # Run the LLM on the working text
            super()._add_translation(working_block)

            # Update metadata to include for all runs
            block.retries += working_block.retries
            block.cost += working_block.cost
            block.processing_time += working_block.processing_time

            # Update the output text to merge this section's output in
            out_text = self._parser.parse(working_block.text)
            if eval_item_type not in obj:
                obj.update(json.loads(out_text))
            else:
                obj[eval_item_type] = obj[eval_item_type] + json.loads(out_text).get(eval_item_type, [])

        block.text = self._parser.parse(json.dumps(obj))
        block.tokens = self._llm.get_num_tokens(block.text)
        block.translated = True