import copy
import json
import re

from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel

from janus.converter.converter import Converter
from janus.language.block import JanusOutputObject, TranslatedCodeBlock
from janus.language.combine import JsonCombiner
from janus.parsers.eval_parsers.incose_parser import IncoseParser
from janus.parsers.eval_parsers.inline_comment_parser import InlineCommentParser
from janus.parsers.eval_parsers.java_category_parser import LabeledJavaListParser
from janus.parsers.eval_parsers.summary_parser import SummaryParser
from janus.parsers.eval_parsers.uml_parser import UMLParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class Evaluator(Converter):
    """Evaluator

    A class that performs an LLM self evaluation"
    "on an input target, with an associated prompt.

    Current valid evaluation types:
    ['incose', 'comments', 'uml']

    """

    def __init__(self, eval_items_per_request: int | None = None, **kwargs) -> None:
        """Initialize the Evaluator class

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set.
            model_arguments: Additional arguments to pass to the LLM constructor.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        kwargs.update(use_janus_inputs=True)
        super().__init__(**kwargs)
        self._eval_items_per_request: int | None = eval_items_per_request
        self._combiner = JsonCombiner()

    def _filter_inputs(self, inputs: list[JanusOutputObject]) -> str:
        """Get single string input according to block types and labels"""
        if self._input_types is not None:
            inputs = [b for b in inputs if b["metadata"]["type"] in self._input_types]
        if self._input_labels is not None:
            inputs = [b for b in inputs if b["metadata"]["label"] in self._input_labels]

        if len(inputs) != 1:
            raise ValueError("Error: ambiguous input to evaluation")

        input = inputs[0]
        if "output" in input:
            return input["output"]

        return self._filter_inputs(input["outputs"])


class RequirementEvaluator(Evaluator):
    """INCOSE Requirement Evaluator

    A class that performs an LLM self evaluation on an input target,
    with an associated prompt.

    The evaluation prompts are for Incose Evaluations

    """

    def __init__(
        self,
        input_types: str | set[str] = set(["requirements"]),
        output_type: str = "requirements_eval",
        **kwargs,
    ) -> None:
        """Initialize the Evaluator class

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set.
            model_arguments: Additional arguments to pass to the LLM constructor.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        super().__init__(input_types=input_types, output_type=output_type, **kwargs)
        self._parser = IncoseParser()
        self._prompt_template_names = ["eval_prompts/incose"]

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

    def _add_translation(self, block: TranslatedCodeBlock) -> None:
        if block.translated:
            return

        if block.original.text is None:
            block.translated = True
            return

        if block.previous_generation is None:
            raise ValueError("Error: cannot evaluate block, no previous generation found")

        # Get original code from the input to requirements generation
        if isinstance(block.previous_generation["input"], str):
            input_str = block.previous_generation["input"]
        elif "output" in block.previous_generation["input"]:
            input_str = block.previous_generation["input"]["output"]
        else:
            input_str = self._filter_inputs(block.previous_generation["input"]["outputs"])

        requirements = json.loads(block.original.text)

        if not requirements:
            log.debug(f"[{block.name}] Skipping empty output")
            return

        # Requirements list can be a list of lists; flatten
        if isinstance(requirements, list) and isinstance(requirements[0], list):
            requirements = requirements[0]

        # Collect source input code and requirement outputs together
        block.original.text = json.dumps(
            dict(
                requirements=requirements,
                code=input_str,
            )
        )

        # If there's not too many comments for a single request, simply
        #  translate as-is
        if (
            not self._eval_items_per_request
            or len(requirements) < self._eval_items_per_request
        ):
            return super()._add_translation(block)

        group_indices = list(range(0, len(requirements), self._eval_items_per_request))
        log.debug(
            f"[{block.name}]"
            f" Block contains more than {self._eval_items_per_request}"
            f" requirements, splitting {len(requirements)} requirements into"
            f" {len(group_indices)} groups"
        )

        translate_obj = {}
        for req_ind in group_indices:
            working_requirements = requirements[
                req_ind : req_ind + self._eval_items_per_request
            ]

            temp_block = copy.deepcopy(block)
            temp_block.original.text = json.dumps(
                dict(
                    requirements=working_requirements,
                    code=input_str,
                )
            )

            super()._add_translation(temp_block)

            translate_obj.update(json.loads(temp_block.text))

        block.text = json.dumps(translate_obj)
        block.tokens = self._llm.get_num_tokens(block.text)
        block.translated = True


class InlineCommentEvaluator(Evaluator):
    """Inline Comment Evaluator

    A class that performs an LLM self evaluation on inline comments,
    with an associated prompt.
    """

    def __init__(
        self,
        input_types: str | set[str] = set(["cloze_comments"]),
        output_type: str = "cloze_comments_eval",
        **kwargs,
    ) -> None:
        """Initialize the Evaluator class

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set.
            model_arguments: Additional arguments to pass to the LLM constructor.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        super().__init__(input_types=input_types, output_type=output_type, **kwargs)
        self._parser = InlineCommentParser()
        self._prompt_template_names = ["eval_prompts/inline_comments"]

    def _process_comments(
        self, input_str: str, generated_comments: dict[str, str]
    ) -> tuple[str, int]:
        comment_patterns = [
            (r"<BLOCK_COMMENT (\w{8})>", "<BLOCK_COMMENT {}>", "<BLOCK_COMMENT {}>"),
            (r"<INLINE_COMMENT (\w{8})>", "<INLINE_COMMENT {}>", "<INLINE_COMMENT {}>"),
            (r"<MODULE (\w{8})>", "<MODULE {}>", "<BLOCK_COMMENT {}>"),
        ]
        missing_comments = 0
        for pattern, find_template, repl_template in comment_patterns:
            matches = re.findall(pattern, input_str)

            for comment_id in matches:
                find_tag = find_template.format(comment_id)
                repl_tag = repl_template.format(comment_id)

                if comment_id not in generated_comments:
                    missing_comments += 1
                comment = generated_comments.get(comment_id, "[comment missing]")
                comment = comment.replace("\n", "\\n")

                # Replace the tag in the code with the comment appended.
                input_str = input_str.replace(find_tag, f"{repl_tag} {comment}")
        processed_str = re.sub(r"\s*<JANUS_PARTITION>\s*\n", "\n", input_str)
        return processed_str.strip("\n"), missing_comments

    def _add_translation(self, block: TranslatedCodeBlock) -> None:
        """Provided block must have a previous_generations list, so that it can
        access the input text with the placeholders, as well as the output
        text with the filled comments
        """
        if block.translated:
            return

        if block.original.text is None:
            block.translated = True
            return

        if block.previous_generation is None:
            raise ValueError(
                "Error: cannot evaluate block, no previous generations found"
            )

        # Get input to comment generation, which includes the original code
        #  and all the tagged comment placeholders
        if isinstance(block.previous_generation["input"], str):
            input_str = block.previous_generation["input"]
        elif "output" in block.previous_generation["input"]:
            input_str = block.previous_generation["input"]["output"]
        else:
            input_str = self._filter_inputs(block.previous_generation["input"]["outputs"])

        generated_comments = json.loads(block.original.text)

        # Process input to insert the generated comments after the tagged placeholders
        processed_input, missing_comments = self._process_comments(
            input_str, generated_comments
        )
        if missing_comments:
            log.info(f"[{block.name}] Warning: missing {missing_comments} comments")

        comment_pattern = r"<(?:INLINE|BLOCK)_COMMENT \w{8}>.*$"
        comments = list(re.finditer(comment_pattern, processed_input, flags=re.MULTILINE))
        if not comments:
            log.info(f"[{block.name}] Skipping commentless block")
            return

        block.original.text = processed_input

        # If there's not too many comments for a single request, simply
        #  translate as-is
        if (
            self._eval_items_per_request is None
            or len(comments) < self._eval_items_per_request
        ):
            return super()._add_translation(block)

        group_indices = list(range(0, len(comments), self._eval_items_per_request))
        log.debug(
            f"[{block.name}]"
            f" Block contains more than {self._eval_items_per_request}"
            f" comments, splitting {len(comments)} comments into"
            f" {len(group_indices)} groups"
        )

        translate_obj = {}
        for comment_ind in group_indices:
            working_comments = comments[
                comment_ind : comment_ind + self._eval_items_per_request
            ]
            start_idx = working_comments[0].start()
            end_idx = working_comments[-1].end()
            prefix = processed_input[:start_idx]
            keeper = processed_input[start_idx:end_idx]
            suffix = processed_input[end_idx:]

            # Strip all comment placeholders outside of the section of interest
            prefix = re.sub(comment_pattern, "", prefix, flags=re.MULTILINE)
            suffix = re.sub(comment_pattern, "", suffix, flags=re.MULTILINE)

            temp_block = copy.deepcopy(block)
            temp_block.original.text = prefix + keeper + suffix

            super()._add_translation(temp_block)

            translate_obj.update(json.loads(temp_block.text))

        block.text = json.dumps(translate_obj)
        block.tokens = self._llm.get_num_tokens(block.text)
        block.translated = True


class SummaryEvaluator(Evaluator):
    """Summary Evaluator

    A class that performs an LLM self evaluation on code summaries,
    with an associated prompt.
    """

    def __init__(
        self,
        input_types: str | set[str] = set(["documentation"]),
        output_type: str = "summary_eval",
        **kwargs,
    ) -> None:
        """Initialize the Evaluator class

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set.
            model_arguments: Additional arguments to pass to the LLM constructor.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        super().__init__(input_types=input_types, output_type=output_type, **kwargs)
        self._parser = SummaryParser()
        self._prompt_template_names = ["eval_prompts/summary"]

    def _input_runnable(self) -> Runnable:
        def _get_code(json_text: str) -> str:
            return json.loads(json_text)["code"]

        def _get_summary(json_text: str) -> str:
            return json.loads(json_text)["summary"]

        return RunnableLambda(self._parser.parse_input) | RunnableParallel(
            SOURCE_CODE=_get_code,
            CODE_SUMMARY=_get_summary,
            context=self._retriever,
        )

    def _add_translation(self, block: TranslatedCodeBlock) -> None:
        if block.translated:
            return

        if block.original.text is None:
            block.translated = True
            return

        if block.previous_generation is None:
            raise ValueError(
                "Error: cannot evaluate block, no previous generations found"
            )

        # Get original code from the input to summary generation
        if isinstance(block.previous_generation["input"], str):
            input_str = block.previous_generation["input"]
        elif "output" in block.previous_generation["input"]:
            input_str = block.previous_generation["input"]["output"]
        else:
            input_str = self._filter_inputs(block.previous_generation["input"]["outputs"])

        summary = block.original.text

        if not summary:
            log.debug(f"[{block.name}] Skipping empty output")
            return

        # Collect source input code and summary outputs together
        block.original.text = json.dumps(
            dict(
                summary=summary,
                code=input_str,
            )
        )
        super()._add_translation(block)


class UMLEvaluator(Evaluator):
    """PLANTUML Diagram Evaluator

    A class that performs an LLM self evaluation on PLANTUML diagrams,
    with an associated prompt.
    """

    def __init__(
        self,
        input_types: str | set[str] = set(["diagram"]),
        output_type: str = "uml_eval",
        **kwargs,
    ) -> None:
        """Initialize the Evaluator class

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set.
            model_arguments: Additional arguments to pass to the LLM constructor.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        super().__init__(input_types=input_types, output_type=output_type, **kwargs)
        self._parser = UMLParser()
        self._prompt_template_names = ["eval_prompts/uml"]

    def _input_runnable(self) -> Runnable:
        def _get_code(json_text: str) -> str:
            return json.loads(json_text)["code"]

        def _get_diagrams(json_text: str) -> str:
            return json.loads(json_text)["diagrams"]

        return RunnableLambda(self._parser.parse_input) | RunnableParallel(
            SOURCE_CODE=_get_code,
            PLANTUML_DIAGRAM=_get_diagrams,
            context=self._retriever,
        )

    def _add_translation(self, block: TranslatedCodeBlock) -> None:
        if block.translated:
            return

        if block.original.text is None:
            block.translated = True
            return

        if block.previous_generation is None:
            raise ValueError(
                "Error: cannot evaluate block, no previous generations found"
            )

        # Get original code from the input to requirements generation
        if isinstance(block.previous_generation["input"], str):
            input_str = block.previous_generation["input"]
        elif "output" in block.previous_generation["input"]:
            input_str = block.previous_generation["input"]["output"]
        else:
            input_str = self._filter_inputs(block.previous_generation["input"]["outputs"])

        diagrams = block.original.text

        if not diagrams:
            log.debug(f"[{block.name}] Skipping empty output")
            return

        # Collect source code and diagram outputs together
        block.original.text = json.dumps(
            dict(
                diagrams=diagrams,
                code=input_str,
            )
        )
        super()._add_translation(block)


class JavaCategoryEvaluator(Evaluator):
    """Java Category Evaluator

    A class that performs LLM-based labelling/evals of llm generated Java,
    appends line numbers so the llm can track things in prompts.
    """

    def __init__(
        self,
        eval_items_per_request: int | None = None,  # not used
        input_types: str | set[str] = None,  # disable filtering by type
        output_type: str = "java_category_eval",
        **kwargs,
    ) -> None:
        """Initialize the Evaluator class

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set.
            model_arguments: Additional arguments to pass to the LLM constructor.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        super().__init__(input_types=input_types, output_type=output_type, **kwargs)
        self._parser = LabeledJavaListParser()
        self._prompt_template_names = ["eval_prompts/java_category"]

    def _add_translation(self, block: TranslatedCodeBlock) -> None:
        if block.translated:
            return

        if block.original.text is None:
            block.translated = True
            return

        if block.previous_generation is None:
            raise ValueError("Error: cannot evaluate block, no previous generation found")

        # Get the raw code from the previous generation
        if isinstance(block.previous_generation["input"], str):
            raw_code = block.previous_generation["input"]
        elif "output" in block.previous_generation["input"]:
            raw_code = block.previous_generation["input"]["output"]
        else:
            raw_code = self._filter_inputs(block.previous_generation["input"]["outputs"])

        if not raw_code.strip():
            log.warning(f"[{block.name}] Warning: empty 'outputs' field, skipping block")
            return

        log.debug(f"[{block.name}] Code for evals: {len(raw_code.splitlines())} lines")

        evaluation_output = block.original.text

        if not evaluation_output:
            log.debug(f"[{block.name}] Skipping empty output")
            return

        # Combine the raw code and evaluation output into the block's original text
        block.original.text = json.dumps(
            dict(
                code=raw_code,
                evaluation=evaluation_output,
            )
        )
        super()._add_translation(block)
