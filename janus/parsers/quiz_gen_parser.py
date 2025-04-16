import json
import random

from langchain_core.messages import BaseMessage

from janus.parsers.parser import JanusParser, JanusParserException
from janus.utils.logger import create_logger

log = create_logger(__name__)


class QuizGenParser(JanusParser):
    language: str
    topic: str

    def shuffle_options(self, questions):
        for question in questions:
            # Extract options and correct answer number
            options = [question[f"option-{i+1}"] for i in range(4)]
            correct_answer_index = int(question["correct-answer-number"]) - 1
            # Shuffle options
            shuffled_options = options[:]
            random.shuffle(shuffled_options)
            # Find new correct answer index
            new_correct_answer_index = shuffled_options.index(
                options[correct_answer_index]
            )
            # Update question with shuffled options and new correct answer
            for i in range(4):
                question[f"option-{i+1}"] = shuffled_options[i]
            question["correct-answer-number"] = str(new_correct_answer_index + 1)
        return questions

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
        # Shuffle the answer options
        data = self.shuffle_options(data)
        # Add a question ID to each question, put as the first field in each object
        updated_data = []
        for index, question in enumerate(data, start=1):
            ordered_question = {"question-id": str(index)}
            ordered_question.update(question)
            ordered_question["topic"] = self.topic
            updated_data.append(ordered_question)
        log.info(f"VALID JSON object. Output:\n{text}")
        return json.dumps(updated_data)

    def get_format_instructions(self) -> str:
        return "Output must be a JSON array of objects."
