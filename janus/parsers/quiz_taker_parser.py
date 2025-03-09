import json

from langchain_core.messages import BaseMessage

from janus.parsers.parser import JanusParser, JanusParserException
from janus.utils.logger import create_logger

log = create_logger(__name__)


class QuizTakerParser(JanusParser):
    language: str

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)
        original_text = text
        log.info(f"TEST OUTPUT. Output:\n{text}")
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
        # TODO Faith add shuffling here
        log.info(f"VALID JSON object. Output:\n{text}")
        return json.dumps(data)

    def get_format_instructions(self) -> str:
        return "Output must be a JSON array of objects."
