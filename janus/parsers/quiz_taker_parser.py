import json

from langchain_core.messages import BaseMessage

from janus.parsers.parser import JanusParser, JanusParserException
from janus.utils.logger import create_logger

log = create_logger(__name__)


class QuizTakerParser(JanusParser):
    language: str

    def extract_json_content(self, text):
        json_content = None
        start_index = 0
        while True:
            # Find the next opening bracket
            json_start_index = text.find("[", start_index)
            if json_start_index == -1:
                break
            # Find the next closing bracket after the opening bracket
            json_end_index = text.find("]", json_start_index)
            if json_end_index == -1:
                break
            # Extract the content between the brackets
            potential_json = text[json_start_index:json_end_index + 1]
            try:
                json.loads(potential_json)
                json_content = potential_json
                break
            except json.JSONDecodeError:
                start_index = json_end_index + 1
        return json_content

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)
        original_text = text
        text = self.extract_json_content(text)
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
