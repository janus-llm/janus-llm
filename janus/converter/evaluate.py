import json
import re
from pathlib import Path

from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel

from janus.converter.converter import Converter
from janus.language.block import CodeBlock, TranslatedCodeBlock
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
                `OPENAI_API_KEY` environment variable must be set.
            model_arguments: Additional arguments to pass to the LLM constructor.
            max_prompts: The maximum number of prompts to try before giving up.
        """
        kwargs.update(use_janus_inputs=True)
        super().__init__(**kwargs)
        self._combiner = JsonCombiner()
        self._load_parameters()


class RequirementEvaluator(Evaluator):
    """INCOSE Requirement Evaluator

    A class that performs an LLM self evaluation on an input target,
    with an associated prompt.

    The evaluation prompts are for Incose Evaluations

    """

    def __init__(
        self,
        eval_items_per_request: int | None = None,
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
        kwargs.update(input_types=input_types, output_type=output_type)
        super().__init__(**kwargs)
        self.eval_items_per_request = eval_items_per_request
        self._parser = IncoseParser()
        self.set_prompts("eval_prompts/incose")

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

    def translate_block(self, input_block: CodeBlock, failure_path: Path | None = None):
        if len(input_block.previous_generations) == 0:
            raise ValueError(
                "Error: Evaluating requirements without previous generations"
            )
        if isinstance(input_block.previous_generations[-1], dict):
            input_str = input_block.previous_generations[-1]["input"]
        else:
            input_str = input_block.previous_generations[-1].original.text
        requirements = json.loads(input_block.text)
        # The requirements are often a list of lists
        if isinstance(requirements[0], list):
            requirements = requirements[0]
        if not requirements:
            log.debug(f"[{input_block.name}] Skipping empty output")
            return []
        if (
            not self.eval_items_per_request
            or len(requirements) < self.eval_items_per_request
        ):
            obj_str = json.dumps(
                dict(
                    requirements=requirements,
                    code=input_str,
                )
            )
            temp_block = self._split_text(obj_str, input_block.name)
            translated_block = super().translate_block(temp_block, failure_path)
            translated_block.original = input_block
            translated_block.previous_generations = input_block.previous_generations
            return translated_block
        else:
            translated_blocks = []
            translated_str: str
            translate_obj = {}
            for i in range(0, len(requirements), self.eval_items_per_request):
                working_requirements = requirements[i : i + self.eval_items_per_request]
                obj_str = json.dumps(
                    dict(
                        requirements=working_requirements,
                        code=input_str,
                    )
                )
                temp_block = self._split_text(obj_str, input_block.name)
                translated_block = super().translate_block(temp_block, failure_path)
                translated_blocks.append(translated_block)
                translate_obj.update(json.loads(translated_block.text))
                translated_str = json.dumps(translate_obj)

        translated_block = TranslatedCodeBlock(
            input_block,
            self._target_language,
            self,
            self._output_type,
            self._output_label,
        )
        translated_block.text = translated_str
        translated_block.children = translated_blocks
        translated_block.tokens = self._llm.get_num_tokens(translated_str)
        translated_block.translated = True
        return translated_block


class InlineCommentEvaluator(Evaluator):
    """Inline Comment Evaluator

    A class that performs an LLM self evaluation on inline comments,
    with an associated prompt.
    """

    def __init__(
        self,
        eval_items_per_request: int | None = None,
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
        kwargs.update(input_types=input_types, output_type=output_type)
        super().__init__(**kwargs)
        self._combiner = JsonCombiner()
        self._parser = InlineCommentParser()
        self.set_prompts("eval_prompts/inline_comments")
        self.eval_items_per_request = eval_items_per_request
        self._load_parameters()

    def _process_comments(self, input_str: str, generated_comments: dict[str, str]):
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

    def translate_block(self, input_block: CodeBlock, failure_path: Path | None = None):
        comment_pattern = r"<(?:INLINE|BLOCK)_COMMENT \w{8}>.*$"
        if len(input_block.previous_generations) == 0:
            raise ValueError(
                "Error: cannot evaluate block, no previous generations found"
            )
        if isinstance(input_block.previous_generations[-1], dict):
            input_str = input_block.previous_generations[-1]["input"]
        else:
            input_str = input_block.previous_generations[-1].original.text
        generated_comments = json.loads(input_block.text)
        processed_input, missing_comments = self._process_comments(
            input_str, generated_comments
        )
        if missing_comments:
            log.info(f"[{input_block.name}] Warning: missing {missing_comments} comments")
        comments = list(re.finditer(comment_pattern, processed_input, flags=re.MULTILINE))
        if not comments:
            log.info(f"[{input_block.name}] Skipping commentless block")
            return []
        if (
            self.eval_items_per_request is None
            or len(comments) < self.eval_items_per_request
        ):
            temp_block = self._split_text(processed_input, input_block.name)
            translated_block = super().translate_block(temp_block, failure_path)
            translated_block.original = input_block
            translated_block.previous_generations = input_block.previous_generations
            return translated_block
        else:
            comment_group_indices = list(
                range(0, len(comments), self.eval_items_per_request)
            )
            log.debug(
                f"[{input_block.name}]"
                f" Block contains more than {self.eval_items_per_request}"
                f" comments, splitting {len(comments)} comments into"
                f" {len(comment_group_indices)} groups"
            )
            translated_blocks = []
            translated_str: str
            translate_obj = {}
            for comment_ind in comment_group_indices:
                working_comments = comments[
                    comment_ind : comment_ind + self.eval_items_per_request
                ]
                start_idx = working_comments[0].start()
                end_idx = working_comments[-1].end()
                prefix = processed_input[:start_idx]
                keeper = processed_input[start_idx:end_idx]
                suffix = processed_input[end_idx:]

                # Strip all comment placeholders outside of the section of interest
                prefix = re.sub(comment_pattern, "", prefix, flags=re.MULTILINE)
                suffix = re.sub(comment_pattern, "", suffix, flags=re.MULTILINE)
                temp_block = self._split_text(prefix + keeper + suffix, input_block.name)
                translated_block = super().translate_block(temp_block, failure_path)
                translated_blocks.append(translated_block)
                translate_obj.update(json.loads(translated_block.text))
                translated_str = json.dumps(translate_obj)
            translated_block = TranslatedCodeBlock(
                input_block,
                self._target_language,
                self,
                self._output_type,
                self._output_label,
            )
            translated_block.children = translated_blocks
            translated_block.text = translated_str
            translated_block.tokens = self._llm.get_num_tokens(translated_str)
            translated_block.translated = True
            return translated_block
