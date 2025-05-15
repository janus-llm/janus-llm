import json

from langchain_core.messages import BaseMessage

from janus.language.block import CodeBlock
from janus.parsers.parser import JanusParser, JanusParserException
from janus.utils.logger import create_logger

log = create_logger(__name__)


class QuizTakerParser(JanusParser):
    language: str

    def parse_input(self, block: CodeBlock) -> str:
        # Get code input from generation step
        if block.previous_generation is None:
            # TODO: Define an exception type that can be caught and skipped
            raise ValueError("Error: Taking quiz without code context")

        prev_gen = block.previous_generation
        input_str = json.loads(prev_gen["input"])

        data = json.loads(block.text)  # type: ignore
        for question in data:
            if "correct-answer-number" in question:
                del question["correct-answer-number"]

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
        # strip out anything before or after the json
        json_start_index = text.find("[")
        json_end_index = text.rfind("]") + 1
        # If the opening bracket is found, slice the string from that index
        if (
            json_start_index != -1
            and json_end_index != -1
            and json_end_index > json_start_index
        ):
            json_content = text[json_start_index:json_end_index]
            text = json_content
        else:
            text = None  # Return None if no JSON content is found
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            log.debug(f"Invalid JSON object. Output:\n{text}")
            raise JanusParserException(
                original_text, f"Got invalid JSON object. Error: {e}"
            )
        if not isinstance(data, list):
            raise JanusParserException(
                original_text,
                f"Got invalid return object. Expected a dictionary, but got {type(data)}",
            )
        return json.dumps(data)

    def get_format_instructions(self) -> str:
        return "Output must be a JSON array of objects."
