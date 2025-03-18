import json

from langchain_core.messages import BaseMessage

from janus.parsers.parser import JanusParser, JanusParserException
from janus.utils.logger import create_logger

log = create_logger(__name__)


class QuizGenParser(JanusParser):
    language: str

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)
        original_text = text
        #strip out anything before or after the json
        json_start_index = text.find('[')
        json_end_index = text.rfind(']') + 1
        # If the opening bracket is found, slice the string from that index
        if json_start_index != -1 and json_end_index != -1 and json_end_index > json_start_index:
            json_content = text[json_start_index:json_end_index]
            text = json_content
        else:
            text = None  # Return None if no JSON content is found
        log.info(f"ORIGINAL TEXT:\n {original_text} \n")
        log.info(f"STRIPPED TEXT:\n {text} \n")
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
        # Add a question ID to each question, put as the first field in each object
        updated_data = []
        for index, question in enumerate(data, start=1):
            ordered_question = {"question-id": str(index)}
            ordered_question.update(question)
            updated_data.append(ordered_question)
        log.info(f"VALID JSON object. Output:\n{text}")
        return json.dumps(updated_data)

    def get_format_instructions(self) -> str:
        return "Output must be a JSON array of objects."
