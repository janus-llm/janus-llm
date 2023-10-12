import json
import re
from collections import defaultdict
from typing import Any, Set

from langchain.schema.output_parser import BaseOutputParser

from ..language.block import CodeBlock
from ..language.combine import Combiner
from ..utils.logger import create_logger

log = create_logger(__name__)


PARSER_TYPES: Set[str] = {"code", "text", "eval"}


class JanusParser(BaseOutputParser):
    def parse(self, text: str) -> str:
        return text

    def parse_combined_output(self, text: str) -> str:
        return text

    def score(self, input_block: CodeBlock, output_text: str) -> float:
        """Validate and score the output text based upon the input CodeBlock.
        Output is a score between 0 and 1.

        Arguments:
            input_block: A `CodeBlock` representing the input to the LLM
            output_text: The parsed text returned by the LLM

        Returns:
            A score between 0 and 1 (inclusive). A score of 1.0 indicates that
            the given text is fully acceptable, and no further attempts
            should be made.
        """
        return 1.0

    def get_format_instructions(self) -> str:
        return "No format requirements"

    @property
    def _type(self) -> str:
        return type(self).__name__


class CodeParser(JanusParser):
    language: str

    def parse(self, text: str) -> str:
        pattern = rf"```[^\S\r\n]*(?:{self.language}[^\S\r\n]*)?\n?(.*?)\n*```"
        code = re.search(pattern, text, re.DOTALL)
        if code is None:
            raise ValueError("Code not find code between triple backticks")
        return code.group(1)

    def score(self, input_block: CodeBlock, output_text: str) -> float:
        """The score for translated code is the percentage of this block's
        children which are present in the output
        """
        if not input_block.children:
            return 1.0

        missing_children = []
        for child in input_block.children:
            if not Combiner.contains_child(output_text, child):
                missing_children.append(child.id)

        if missing_children:
            log.warning(
                f"[{input_block.name}] Child placeholders not present in text: "
                f"{missing_children}"
            )
            log.debug(f"Code:\n{output_text}")

        return 1.0 - len(missing_children) / len(input_block.children)

    def get_format_instructions(self) -> str:
        return "Output must contain text contained within triple backticks."


class JsonLinesParser(JanusParser):
    def parse(self, text: str) -> str:
        string = r"\"\w+\""
        number = r"-?\d+(?:\.\d*)?"
        json_value = rf"(?:{string}|{number})"
        json_line = rf"\s*{string} *: *{json_value},?\s*"
        pattern = "({" + rf"(?:{json_line})+" + "})"
        matches = list(re.finditer(pattern, text, re.DOTALL))
        if not matches:
            raise ValueError("Could not find JSON output")

        output_strings = [json.dumps(json.loads(match.group(1))) for match in matches]
        return "\n".join(output_strings)

    def parse_combined_output(self, text: str) -> str:
        return self.parse(text)

    def get_format_instructions(self) -> str:
        return "Output must contain one or more JSON-formatted blocks."


class JsonParser(JsonLinesParser):
    def parse(self, text: str) -> str:
        jsonl_text = super().parse(text)
        if len(jsonl_text.split("\n")) > 1:
            raise ValueError("Multiple JSON objects found")

        return jsonl_text

    def parse_combined_output(self, text: str) -> str:
        jsonl_text = JsonLinesParser.parse(self, text)
        json_lines = jsonl_text.split("\n")
        output_obj = {i: json.loads(t) for i, t in enumerate(json_lines)}
        return json.dumps(output_obj)

    def get_format_instructions(self) -> str:
        return "Output must contain exactly one JSON-formatted block."


class EvaluationParser(JsonParser):
    expected_keys: Set[str]

    def __init__(self, expected_keys: Set[str], **kwargs: Any):
        super().__init__(expected_keys=expected_keys, **kwargs)
        self.expected_keys = {k.lower() for k in expected_keys}

    def parse(self, text: str) -> str:
        """Parse the JSON object, convert keys to lowercase, filter out
        unexpected keys
        """
        json_text = super().parse(text)
        obj = json.loads(json_text)
        obj = {k.lower(): v for k, v in obj.items()}
        obj = {k: v for k, v in obj.items() if k in self.expected_keys}
        return json.dumps(obj)

    def parse_combined_output(self, text: str) -> str:
        json_text = super().parse_combined_output(text)
        multi_obj = json.loads(json_text)
        n_evals = len(multi_obj)

        output_obj = defaultdict(float)
        for obj in multi_obj.values():
            for k, v in obj.items():
                output_obj[k] += v / n_evals

        return json.dumps(output_obj)

    def score(self, input_block: CodeBlock, output_text: str) -> float:
        """The score for the output text is the percentage of expected keys
        that are present in the json object. Non-numeric values count for
        half.
        """
        obj = json.loads(output_text)

        expected_keys = self.expected_keys.intersection(obj.keys())
        missing_keys = self.expected_keys.difference(obj.keys())
        if missing_keys:
            log.warning(f"[{input_block.name}] Expected keys missing: {missing_keys}")

        non_numerics = {k: v for k, v in obj.items() if not isinstance(v, (int, float))}
        if non_numerics:
            log.warning(f"[{input_block.name}] Non-numeric values: {non_numerics}")

        if missing_keys or non_numerics:
            log.debug(f"Text:\n{output_text}")

        return (len(expected_keys) - len(non_numerics) * 0.5) / len(self.expected_keys)

    def get_format_instructions(self) -> str:
        return (
            "Output must contain exactly one JSON-formatted block. The JSON "
            "object should contain only the keys contained in the provided "
            "expected_keys set (if any), and values should be numeric."
        )
