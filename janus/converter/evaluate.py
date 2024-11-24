import json
import re
from copy import deepcopy

from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel

from janus.converter.converter import Converter
from janus.language.block import TranslatedCodeBlock
from janus.language.combine import JsonCombiner
from janus.parsers.eval_parsers.incose_parser import IncoseParser
from janus.parsers.eval_parsers.inline_comment_parser import InlineCommentParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class Evaluator(Converter):
    """Evaluator

    A class that performs an LLM self evaluation"
    "on an input target, with an associated prompt.

    Current valid evaluation types:
    ['incose', 'comments']

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


class RequirementEvaluator(Evaluator):
    """INCOSE Requirement Evaluator

    A class that performs an LLM self evaluation on an input target,
    with an associated prompt.

    The evaluation prompts are for Incose Evaluations

    """

    def __init__(self, eval_items_per_request: int | None = None, **kwargs) -> None:
        """Initialize the Evaluator class

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set and the
                `OPENAI_ORG_ID` environment variable should be set if needed.
            model_arguments: Additional arguments to pass to the LLM constructor.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        super().__init__(**kwargs)
        self.eval_items_per_request = eval_items_per_request
        self._parser = IncoseParser()
        self.set_prompt("eval_prompts/incose")

    def _input_runnable(self) -> Runnable:
        def _get_code(json_text: str) -> str:
            return json.loads(json_text)["code"]

        def _get_reqs(json_text: str) -> str:
            return json.dumps(json.loads(json_text)["requirements"])

        return RunnableLambda(self._parser.parse_input) | RunnableParallel(
            SOURCE_CODE=_get_code,
            REQUIREMENTS=_get_reqs,
            context=self._retriever,
        )

    def _add_translation(self, block: TranslatedCodeBlock):
        if block.translated:
            return

        if block.original.text is None:
            block.translated = True
            return

        if self.eval_items_per_request is None:
            return super()._add_translation(block)

        input_obj = json.loads(block.original.text)
        requirements = input_obj.get("requirements", [])

        if not requirements:
            log.debug(f"[{block.name}] Skipping empty block")
            block.translated = True
            block.text = None
            block.complete = True
            return

        # For some reason requirements objects are in nested lists?
        while isinstance(requirements[0], list):
            requirements = [r for lst in requirements for r in lst]

        if len(requirements) <= self.eval_items_per_request:
            input_obj["requirements"] = requirements
            block.original.text = json.dumps(input_obj)
            return super()._add_translation(block)

        block.processing_time = 0
        block.cost = 0
        block.retries = 0
        obj = {}
        for i in range(0, len(requirements), self.eval_items_per_request):
            # Build a new TranslatedBlock using the new working text
            working_requirements = requirements[i : i + self.eval_items_per_request]
            working_copy = deepcopy(block.original)
            working_obj = json.loads(working_copy.text)  # type: ignore
            working_obj["requirements"] = working_requirements
            working_copy.text = json.dumps(working_obj)
            working_block = TranslatedCodeBlock(working_copy, self._target_language)

            # Run the LLM on the working text
            super()._add_translation(working_block)

            # Update metadata to include for all runs
            block.retries += working_block.retries
            block.cost += working_block.cost
            block.processing_time += working_block.processing_time

            # Update the output text to merge this section's output in
            obj.update(json.loads(working_block.text))

        block.text = json.dumps(obj)
        block.tokens = self._llm.get_num_tokens(block.text)
        block.translated = True

        log.debug(
            f"[{block.name}] Output code:\n{json.dumps(json.loads(block.text), indent=2)}"
        )


class InlineCommentEvaluator(Evaluator):
    """Inline Comment Evaluator

    A class that performs an LLM self evaluation on inline comments,
    with an associated prompt.
    """

    def __init__(self, eval_items_per_request: int | None = None, **kwargs) -> None:
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
        self._parser = InlineCommentParser()
        self.set_prompt("eval_prompts/inline_comments")
        self.eval_items_per_request = eval_items_per_request

    def _add_translation(self, block: TranslatedCodeBlock):
        if block.translated:
            return

        if block.original.text is None:
            block.translated = True
            return

        if self.eval_items_per_request is None:
            return super()._add_translation(block)

        comment_pattern = r"<(?:INLINE|BLOCK)_COMMENT \w{8}>.*$"
        comments = list(
            re.finditer(comment_pattern, block.original.text, flags=re.MULTILINE)
        )

        if not comments:
            log.info(f"[{block.name}] Skipping commentless block")
            block.translated = True
            block.text = None
            block.complete = True
            return

        if len(comments) <= self.eval_items_per_request:
            return super()._add_translation(block)

        comment_group_indices = list(range(0, len(comments), self.eval_items_per_request))
        log.debug(
            f"[{block.name}] Block contains more than {self.eval_items_per_request}"
            f" comments, splitting {len(comments)} comments into"
            f" {len(comment_group_indices)} groups"
        )

        block.processing_time = 0
        block.cost = 0
        block.retries = 0
        obj = {}
        for i in range(0, len(comments), self.eval_items_per_request):
            # Split the text into the section containing comments of interest,
            #  all the text prior to those comments, and all the text after them
            working_comments = comments[i : i + self.eval_items_per_request]
            start_idx = working_comments[0].start()
            end_idx = working_comments[-1].end()
            prefix = block.original.text[:start_idx]
            keeper = block.original.text[start_idx:end_idx]
            suffix = block.original.text[end_idx:]

            # Strip all comment placeholders outside of the section of interest
            prefix = re.sub(comment_pattern, "", prefix, flags=re.MULTILINE)
            suffix = re.sub(comment_pattern, "", suffix, flags=re.MULTILINE)

            # Build a new TranslatedBlock using the new working text
            working_copy = deepcopy(block.original)
            working_copy.text = prefix + keeper + suffix
            working_block = TranslatedCodeBlock(working_copy, self._target_language)

            # Run the LLM on the working text
            super()._add_translation(working_block)

            # Update metadata to include for all runs
            block.retries += working_block.retries
            block.cost += working_block.cost
            block.processing_time += working_block.processing_time

            # Update the output text to merge this section's output in
            obj.update(json.loads(working_block.text))

        block.text = json.dumps(obj)
        block.tokens = self._llm.get_num_tokens(block.text)
        block.translated = True

        log.debug(
            f"[{block.name}] Output code:\n{json.dumps(json.loads(block.text), indent=2)}"
        )
