import argparse
import csv
import glob
import json
import os
from pathlib import Path


def extract_quiz_attempts(input_file_path):
    """
    Reads the JSON file and extracts quiz attempts based on QuizTaker objects.
    Each QuizTaker object must have an "input" (the quiz answer key from QuizGenerator)
    and an "output" (the quiz taker answers).
    Returns a list of tuples: (taker_answers, answer_key) where each is a list of
    question objects.
    """
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    quiz_attempts = []

    # Check if file has a nested "outputs" list.
    if "outputs" in data:
        # It might be that the QuizTaker objects are nested inside the "outputs" list.
        # For each element, see if it contains an "outputs" list.
        for element in data["outputs"]:
            if isinstance(element, dict) and "outputs" in element:
                for attempt in element["outputs"]:
                    meta = attempt.get("metadata", {})
                    if meta.get("converter_name") == "QuizTaker":
                        # In this structure, the answer key is provided in the
                        # QuizTaker's "input" object.
                        input_section = attempt.get("input", {})
                        if (
                            input_section.get("metadata", {}).get("converter_name")
                            == "QuizGenerator"
                        ):
                            try:
                                # Parse the answer key and taker answers.
                                answer_key = json.loads(input_section.get("output", "[]"))
                                taker_answers = json.loads(attempt.get("output", "[]"))
                            except Exception as e:
                                print(
                                    "Error parsing JSON strings in file "
                                    f"'{input_file_path}':",
                                    e,
                                )
                                continue
                            quiz_attempts.append((taker_answers, answer_key))
    else:
        # Fallback in case the file is a single object with "input" and "output"
        if "input" in data and "output" in data:
            try:
                answer_key = json.loads(data["input"].get("output", "[]"))
                taker_answers = json.loads(data.get("output", "[]"))
            except Exception as e:
                print("Error parsing JSON:", e)
                return []
            quiz_attempts.append((taker_answers, answer_key))
    return quiz_attempts


def combine_attempt(taker_answers, answer_key):
    """
    For one attempt, match the answer key with the taker's answers using question-id.
    Creates a dictionary mapping question-id to the desired CSV row.
    The "split-index" is determined per topic and resets to 1 for each new topic.
    """
    combined = {}
    # Create a dictionary to track the per-topic count.
    topic_counters = {}

    # First, build dictionary from answer key
    for question in answer_key:
        qid = question.get("question-id")
        topic = question.get("topic", "")
        # Reset or increment the counter for this topic.
        if topic in topic_counters:
            topic_counters[topic] += 1
        else:
            topic_counters[topic] = 1
        current_index = topic_counters[topic]

        combined[qid] = {
            "split-index": str(current_index),
            "question-id": qid,
            "topic": topic,
            "question": question.get("question", ""),
            "option-1": question.get("option-1", ""),
            "option-2": question.get("option-2", ""),
            "option-3": question.get("option-3", ""),
            "option-4": question.get("option-4", ""),
            "correct-answer-number": question.get("correct-answer-number", ""),
            "selected-answer-number": "",
            "grading-result": "",
            "reasoning": "",
        }

    # Next, update with taker answers
    for answer in taker_answers:
        qid = answer.get("question-id")
        if qid in combined:
            selected = answer.get("selected-answer-number", "")
            combined[qid]["selected-answer-number"] = selected
            combined[qid]["reasoning"] = answer.get("reasoning", "")
            correct = combined[qid]["correct-answer-number"]
            combined[qid]["grading-result"] = correct == selected
    return combined


def quiz_to_csv(input_file_path: str | Path, output_file_path: str | Path):
    quiz_attempts = extract_quiz_attempts(input_file_path)
    if not quiz_attempts:
        print(f"No valid QuizTaker attempts found in {input_file_path}.")
        return

    headers = [
        "split-index",
        "question-id",
        "topic",
        "question",
        "option-1",
        "option-2",
        "option-3",
        "option-4",
        "correct-answer-number",
        "selected-answer-number",
        "grading-result",
        "reasoning",
    ]

    output_file_path = Path(output_file_path)
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    if output_file_path.exists():
        output_file_path.unlink()

    with open(output_file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for taker_answers, answer_key in quiz_attempts:
            combined = combine_attempt(taker_answers, answer_key)
            for _, row in combined.items():
                writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(
        description="Process QuizTaker JSON file and produce a CSV grading output."
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Path to the input JSON file or directory"
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Path to the output CSV file or directory"
    )
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    if os.path.isfile(input_path):
        quiz_to_csv(input_path, output_path)
    elif os.path.isdir(input_path):
        json_files = glob.glob(os.path.join(input_path, "*.json"))
        if not json_files:
            print("No .json files found in the directory.")
        for json_file in json_files:
            outfile = os.path.join(
                output_path, os.path.basename(json_file).replace(".json", ".csv")
            )
            quiz_to_csv(json_file, outfile)
    else:
        print("Invalid input path. Please provide a valid file or directory.")


if __name__ == "__main__":
    main()
