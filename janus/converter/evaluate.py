import copy
import json
import re
from typing import Iterator

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

    def __init__(self, object_name: str, **kwargs) -> None:
        """Initialize the Evaluator class

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set.
            model_arguments: Additional arguments to pass to the LLM constructor.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        kwargs.update(use_janus_inputs=True)
        super().__init__(**kwargs)
        self._object_name = object_name
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

    def _extract_original_code(self, block: TranslatedCodeBlock) -> str:
        if block.previous_generation is None:
            raise ValueError("Error: cannot evaluate block, no previous generation found")

        if isinstance(block.previous_generation["input"], str):
            input_str = block.previous_generation["input"]
        elif "output" in block.previous_generation["input"]:
            input_str = block.previous_generation["input"]["output"]
        else:
            input_str = self._filter_inputs(block.previous_generation["input"]["outputs"])

        input_str = input_str.strip()
        if not input_str:
            raise ValueError("Error: cannot evaluate block, no previous generation found")

        return input_str

    def _extract_object_to_evaluate(self, block: TranslatedCodeBlock) -> str | None:
        return block.original.text

    def _preprocess_block(self, block: TranslatedCodeBlock) -> None:
        input_str = self._extract_original_code(block)
        object = self._extract_object_to_evaluate(block)

        if not object:
            log.debug(f"[{block.name}] Skipping empty output")
            block.translated = True
            return

        # Collect source input code and requirement outputs together
        block.original.text = json.dumps(
            dict(
                eval_object=object,
                code=input_str,
            )
        )

    def _get_code_from_json(self, json_text: str) -> str:
        return json.loads(json_text)["code"]

    def _get_object_to_evaluate_from_json(self, json_text: str) -> str:
        return json.loads(json_text)["eval_object"]

    def _input_runnable(self) -> Runnable:
        def _get_code(json_text: str) -> str:
            return json.loads(json_text)["code"]

        def _get_eval_obj(json_text: str) -> str:
            return json.dumps(json.loads(json_text)["eval_object"])

        kwargs = {
            "SOURCE_CODE": _get_code,
            self._object_name: _get_eval_obj,
            "context": self._retriever,
        }

        return RunnableLambda(self._parser.parse_input) | RunnableParallel(**kwargs)

    def _add_translation(self, block: TranslatedCodeBlock) -> None:
        if block.translated:
            return
        self._preprocess_block(block)
        super()._add_translation(block)


class MultiObjectEvaluator(Evaluator):
    def __init__(self, eval_items_per_request: int | None = None, **kwargs) -> None:
        """Initialize the Evaluator class

        Arguments:
            model: The LLM to use for translation. If an OpenAI model, the
                `OPENAI_API_KEY` environment variable must be set.
            model_arguments: Additional arguments to pass to the LLM constructor.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        super().__init__(**kwargs)
        self._eval_items_per_request: int | None = eval_items_per_request

    def _get_working_objects(
        self, block: TranslatedCodeBlock
    ) -> Iterator[TranslatedCodeBlock]:
        raise NotImplementedError()

    def _add_translation(self, block: TranslatedCodeBlock) -> None:
        if block.translated:
            return

        self._preprocess_block(block)

        # MultiObjectEvaluators may encounter object with no evaluatable objects,
        #  in which case they will set translated to True
        if block.translated:
            return

        translate_obj = {}
        for obj in self._get_working_objects(block):
            super(Evaluator, self)._add_translation(obj)
            translate_obj.update(json.loads(obj.text))

        block.text = json.dumps(translate_obj)
        block.tokens = self._llm.get_num_tokens(block.text)
        block.translated = True


class RequirementEvaluator(MultiObjectEvaluator):
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
        super().__init__(
            object_name="REQUIREMENTS",
            input_types=input_types,
            output_type=output_type,
            **kwargs,
        )
        self._parser = IncoseParser()
        self._prompt_template_names = ["eval_prompts/incose"]

    def _extract_object_to_evaluate(self, block: TranslatedCodeBlock) -> list[str] | None:
        if block.original.text is None:
            return None

        object = json.loads(block.original.text)
        # Requirements list can be a list of lists; flatten
        if isinstance(object, list) and isinstance(object[0], list):
            object = object[0]

        return object

    def _get_object_to_evaluate_from_json(self, json_text: str) -> str:
        return json.dumps(super()._get_object_to_evaluate_from_json(json_text))

    def _get_working_objects(
        self, block: TranslatedCodeBlock
    ) -> Iterator[TranslatedCodeBlock]:
        if block.original.text is None:
            return

        object = json.loads(block.original.text)
        code = object["code"]
        objects = object["eval_object"]

        if self._eval_items_per_request is None:
            yield block
            return

        if len(objects) <= self._eval_items_per_request:
            yield block
            return

        group_indices = list(range(0, len(objects), self._eval_items_per_request))
        log.debug(
            f"[{block.name}]"
            f" Block contains more than {self._eval_items_per_request}"
            f" objects, splitting {len(objects)} objects into"
            f" {len(group_indices)} groups"
        )

        for req_ind in group_indices:
            working_objects = objects[req_ind : req_ind + self._eval_items_per_request]

            temp_block = copy.deepcopy(block)
            temp_block.original.text = json.dumps(
                dict(
                    requirements=working_objects,
                    code=code,
                )
            )
            yield temp_block


class InlineCommentEvaluator(MultiObjectEvaluator):
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
        super().__init__(
            object_name=None,
            input_types=input_types,
            output_type=output_type,
            **kwargs,
        )
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

    def _extract_object_to_evaluate(
        self, block: TranslatedCodeBlock
    ) -> dict[str, str] | None:
        if block.original.text is None:
            return None
        return json.loads(block.original.text)

    def _preprocess_block(self, block: TranslatedCodeBlock) -> None:
        input_str = self._extract_original_code(block)
        object = self._extract_object_to_evaluate(block)

        if not object:
            log.debug(f"[{block.name}] Skipping empty output")
            block.translated = True
            return

        # Provided block must have a previous_generations list, so that it can
        #  access the input text with the placeholders, as well as the output
        #  text with the filled comments
        # Process input to insert the generated comments after the tagged placeholders
        processed_input, missing_comments = self._process_comments(
            input_str,
            object,
        )
        if missing_comments:
            log.info(f"[{block.name}] Warning: missing {missing_comments} comments")

        comment_pattern = r"<(?:INLINE|BLOCK)_COMMENT \w{8}>.*$"
        comments = list(re.finditer(comment_pattern, processed_input, flags=re.MULTILINE))
        if not comments:
            log.info(f"[{block.name}] Skipping commentless block")
            block.translated = True
            return

        comments_start_end_indices = [
            [comment.start(), comment.end()] for comment in comments
        ]

        # Collect source processed code and comments together
        block.original.text = json.dumps(
            dict(
                eval_object=comments_start_end_indices,
                code=processed_input,
            )
        )

    def _get_working_objects(
        self, block: TranslatedCodeBlock
    ) -> Iterator[TranslatedCodeBlock]:
        if block.original.text is None:
            return

        object = json.loads(block.original.text)
        processed_input = object["code"]
        comments = object["eval_object"]

        block.original.text = processed_input

        if self._eval_items_per_request is None:
            yield block
            return

        if len(comments) <= self._eval_items_per_request:
            yield block
            return

        group_indices = list(range(0, len(comments), self._eval_items_per_request))
        log.debug(
            f"[{block.name}]"
            f" Block contains more than {self._eval_items_per_request}"
            f" comments, splitting {len(comments)} comments into"
            f" {len(group_indices)} groups"
        )

        comment_pattern = r"<(?:INLINE|BLOCK)_COMMENT \w{8}>.*$"

        for comment_ind in group_indices:
            working_comments = comments[
                comment_ind : comment_ind + self._eval_items_per_request
            ]
            start_idx = working_comments[0][0]
            end_idx = working_comments[-1][-1]
            prefix = processed_input[:start_idx]
            keeper = processed_input[start_idx:end_idx]
            suffix = processed_input[end_idx:]

            # Strip all comment placeholders outside of the section of interest
            prefix = re.sub(comment_pattern, "", prefix, flags=re.MULTILINE)
            suffix = re.sub(comment_pattern, "", suffix, flags=re.MULTILINE)

            temp_block = copy.deepcopy(block)
            temp_block.original.text = prefix + keeper + suffix

            yield temp_block

    def _input_runnable(self) -> Runnable:
        return RunnableParallel(
            SOURCE_CODE=self._parser.parse_input,
            context=self._retriever,
        )


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
        super().__init__(
            object_name="CODE_SUMMARY",
            input_types=input_types,
            output_type=output_type,
            **kwargs,
        )
        self._parser = SummaryParser()
        self._prompt_template_names = ["eval_prompts/summary"]


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
        super().__init__(
            object_name="PLANTUML_DIAGRAM",
            input_types=input_types,
            output_type=output_type,
            **kwargs,
        )
        self._parser = UMLParser()
        self._prompt_template_names = ["eval_prompts/uml"]


class JavaCategoryEvaluator(Evaluator):
    """Java Category Evaluator

    A class that performs LLM-based labelling/evals of llm generated Java,
    appends line numbers so the llm can track things in prompts.
    """

    def __init__(
        self,
        input_types: str | set[str] | None = None,  # disable filtering by type
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
        super().__init__(
            object_name="JAVA_CODE",
            input_types=input_types,
            output_type=output_type,
            **kwargs,
        )
        self._use_janus_inputs = False
        self._parser = LabeledJavaListParser()
        self._prompt_template_names = ["eval_prompts/java_category"]

    def _preprocess_block(self, block: TranslatedCodeBlock) -> None:
        block.original.text = self._parser.parse_input(block.original)

    def _input_runnable(self) -> Runnable:
        def _get_eval_obj(json_text: str) -> str:
            return json.dumps(json.loads(json_text)["eval_object"])

        kwargs = {
            self._object_name: _get_eval_obj,
            "context": self._retriever,
        }

        return RunnableParallel(**kwargs)
