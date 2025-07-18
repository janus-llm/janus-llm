import json
import random

from langchain_core.messages import BaseMessage

from janus.parsers.parser import JanusParserException, JsonParser
from janus.utils.logger import create_logger

log = create_logger(__name__)


class QuizGenParser(JsonParser):
    language: str
    topic: str

    n_questions: int = 5
    n_options: int = 4
    option_keys: list[str] = [f"option-{i+1}" for i in range(n_options)]
    expected_keys: set[str] = {
        "discussion",
        "question",
        *option_keys,
    }

    def shuffle_options(self, questions):
        for question in questions:
            # Shuffle options
            shuffle_idx = random.sample(range(self.n_options), k=self.n_options)
            question.update(
                {
                    self.option_keys[i]: question[self.option_keys[j]]
                    for i, j in enumerate(shuffle_idx)
                }
            )

            # Fix the correct answer after the shuffle
            correct_idx = 0
            question["correct-answer-number"] = shuffle_idx.index(correct_idx) + 1

        return questions

    def parse(self, text: str | BaseMessage) -> str:
        if isinstance(text, BaseMessage):
            text = str(text.content)
        original_text = text

        # Strip everything outside the JSON object
        text = JsonParser.parse(self, text)
        try:
            questions = json.loads(text)
        except json.JSONDecodeError as e:
            log.debug(f"Invalid JSON object. Output:\n{text}")
            raise JanusParserException(
                original_text,
                f"Got invalid JSON object. Error: {e}",
            )
        if not isinstance(questions, list):
            raise JanusParserException(
                original_text,
                f"Invalid return object. Expected a list, got {type(questions)}",
            )

        # Validate number of questions
        if len(questions) != self.n_questions:
            raise JanusParserException(
                original_text,
                f"Invalid return object. Expected {self.n_questions} questions,"
                f" got {len(questions)}",
            )

        # Validate question keys
        for i, question in enumerate(questions, start=1):
            # Rename option-1-correct to option-1 in output
            if "option-1-correct" in question:
                question["option-1"] = question.pop("option-1-correct")
            if set(question.keys()) != self.expected_keys:
                raise JanusParserException(
                    original_text,
                    f"Question {i} did not match expected format:\n"
                    f"{json.dumps(question, indent=2)}",
                )

        # Shuffle the answer options
        questions = self.shuffle_options(questions)

        # Add a question ID and Topic to each question as the first fields in each object
        # Put options in numerical order
        updated_data = []
        for index, question in enumerate(questions, start=1):
            updated_data.append(
                {
                    "question-id": str(index),
                    "topic": self.topic,
                    "discussion": question["discussion"],
                    "question": question["question"],
                    "option-1": question["option-1"],
                    "option-2": question["option-2"],
                    "option-3": question["option-3"],
                    "option-4": question["option-4"],
                    "correct-answer-number": question["correct-answer-number"],
                }
            )
        log.debug(f"VALID JSON object. Output:\n{json.dumps(updated_data, indent=2)}")
        return json.dumps(updated_data)

    def get_format_instructions(self) -> str:
        return "Output must be a JSON array of objects."
