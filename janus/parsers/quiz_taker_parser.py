import json

from langchain_core.messages import BaseMessage

from janus.language.block import CodeBlock
from janus.parsers.parser import JanusParserException, JsonParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class QuizTakerParser(JsonParser):
    language: str

    def parse_input(self, block: CodeBlock) -> str:
        # Get code input from generation step
        if block.previous_generation is None:
            # TODO: Define an exception type that can be caught and skipped
            raise ValueError("Error: Taking quiz without code context")

        prev_gen = block.previous_generation
        input_str = prev_gen["input"]

        if isinstance(input_str, dict):
            if "output" in input_str:
                input_str = input_str["output"]
            else:
                log.debug(
                    f"Missing output field in JSON object. Object contents:\n{input_str}"
                )

        data = json.loads(block.text)
        for question in data:
            if "correct-answer-number" in question:
                del question["correct-answer-number"]
            if "discussion" in question:
                del question["discussion"]

        return json.dumps(
            dict(
                quiz=data,
                code=input_str,
            )
        )

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)
        original_text = text
        # Strip everything outside the JSON object
        text = JsonParser.parse(self, text)
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            log.debug(f"Invalid JSON object. Output:\n{text}")
            raise JanusParserException(
                original_text,
                f"Got invalid JSON object. Error: {e}",
            )
        if not isinstance(data, list):
            raise JanusParserException(
                original_text,
                f"Invalid return object. Expected a dict, got {type(data)}",
            )
        return json.dumps(data)

    def get_format_instructions(self) -> str:
        return "Output must be a JSON array of objects."
