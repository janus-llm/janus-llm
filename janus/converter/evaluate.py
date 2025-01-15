import json
import re
from pathlib import Path
from typing import Any

from langchain_core.runnables import Runnable, RunnableLambda, RunnableParallel

from janus.converter.converter import Converter
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
        kwargs.update(janus_inputs=True)
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

    def translate_janus_obj(self, obj: Any, name: str, failure_path: Path | None = None):
        results = []
        for o in obj["outputs"]:
            if isinstance(o, dict):
                results += self.translate_janus_obj(o, name, failure_path)
            elif isinstance(o, str):
                requirements = json.loads(o)
                if not requirements:
                    log.debug(f"[{name}] Skipping empty output")
                    continue
                if (
                    not self.eval_items_per_request
                    or len(requirements) < self.eval_items_per_request
                ):
                    obj_str = json.dumps(
                        dict(
                            requirements=requirements,
                            code=obj["input"],
                        )
                    )
                    results.append(self.translate_text(obj_str, name, failure_path))
                else:
                    for i in range(0, len(requirements), self.eval_items_per_request):
                        working_requirements = requirements[
                            i : i + self.eval_items_per_request
                        ]
                        obj_str = json.dumps(
                            dict(
                                requirements=working_requirements,
                                code=obj["input"],
                            )
                        )
                        results.append(self.translate_text(obj_str, name, failure_path))
            else:
                raise ValueError(f"Error: unable to find janus object: {type(o)}")
        return results


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

    def translate_janus_obj(self, obj: Any, name: str, failure_path: Path | None = None):
        comment_pattern = r"<(?:INLINE|BLOCK)_COMMENT \w{8}>.*$"
        results = []
        input_str = obj["input"]
        for o in obj["outputs"]:
            if isinstance(o, dict):
                results += self.translate_janus_obj(o, name, failure_path)
            elif isinstance(o, str):
                generated_comments = json.loads(o)
                processed_input, missing_comments = self._process_comments(
                    input_str, generated_comments
                )
                if missing_comments:
                    log.info(f"[{name}] Warning: missing {missing_comments} comments")
                comments = list(
                    re.finditer(comment_pattern, processed_input, flags=re.MULTILINE)
                )
                if not comments:
                    log.info(f"[{name}] Skipping commentless block")
                    continue
                if (
                    self.eval_items_per_request is None
                    or len(comments) < self.eval_items_per_request
                ):
                    results.append(
                        self.translate_text(processed_input, name, failure_path)
                    )
                    continue
                comment_group_indices = list(
                    range(0, len(comments), self.eval_items_per_request)
                )
                log.debug(
                    f"[{name}] Block contains more than {self.eval_items_per_request}"
                    f" comments, splitting {len(comments)} comments into"
                    f" {len(comment_group_indices)} groups"
                )
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
                    results.append(
                        self.translate_text(prefix + keeper + suffix, name, failure_path)
                    )
            else:
                raise ValueError(f"Error: unrecognized janus object type: {type(o)}")
        return results
