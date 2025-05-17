import csv
import json
import argparse
from pathlib import Path


def extract_outputs_from_json(file_path):
    # Read the JSON file
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # # Extract the "output" field
    # main_outputs = data.get("output", [])

    # # Extract the previous input
    # intermediate_outputs = []
    # if "input" in data:
    #     for item in data["input"]:
    #         intermediate_outputs.append(item)

    # Extract the "output" field from the top level
    main_outputs = data.get("output", None)

    # Extract the "output" field from the "input" subfield
    intermediate_outputs = None
    if "input" in data and isinstance(data["input"], dict):
        intermediate_outputs = data["input"].get("output", None)

    # Convert JSON strings to Python objects
    main_outputs = [json.loads(main_outputs)]
    intermediate_outputs = [json.loads(intermediate_outputs)]

    main_outputs = [item for sublist in main_outputs for item in sublist]
    intermediate_outputs = [item for sublist in intermediate_outputs for item in sublist]

    return main_outputs, intermediate_outputs


def combine_outputs(main_outputs, intermediate_outputs):
    # Create a dictionary to map question-id to the combined output
    combined_outputs = {}

    # Populate the dictionary with entries from intermediate_outputs
    for entry in intermediate_outputs:
        question_id = entry["question-id"]
        combined_outputs[question_id] = {
            "question-id": question_id,
            "question": entry.get("question", ""),
            "option-1": entry.get("option-1", ""),
            "option-2": entry.get("option-2", ""),
            "option-3": entry.get("option-3", ""),
            "option-4": entry.get("option-4", ""),
            "correct-answer-number": entry.get("correct-answer-number", ""),
            "topic": entry.get("topic", ""),
            "selected-answer-number": None,  # Placeholder for selected-answer-number
            "grading-result": None,  # Placeholder for grading result
            "reasoning": None,  # Placeholder for reasoning
        }

    # Update the dictionary with entries from main_outputs
    for entry in main_outputs:
        question_id = entry["question-id"]
        if question_id in combined_outputs:
            combined_outputs[question_id]["reasoning"] = entry.get("reasoning", "")
            combined_outputs[question_id]["selected-answer-number"] = entry.get(
                "selected-answer-number", ""
            )

            # Determine the grading result
            correct_answer = combined_outputs[question_id]["correct-answer-number"]
            selected_answer = entry.get("selected-answer-number", "")
            combined_outputs[question_id]["grading-result"] = (
                correct_answer == selected_answer
            )

    return combined_outputs


def quiz_to_csv(quiz: dict, file_path: str | Path):
    # Define the headers based on the keys of the dictionary entries
    headers = [
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

    # Ensure the file path is a Path object
    file_path = Path(file_path)
    # Create the directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)
    # Check if the file already exists
    if file_path.exists():
        # Remove the existing file
        file_path.unlink()

    # Open the file for writing
    with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write the header
        writer.writeheader()

        # Write each row
        for _, entry in quiz.items():
            writer.writerow(entry)

# Parse input and output filepath args
parser = argparse.ArgumentParser(description="Process input and output files.")
parser.add_argument("-i", "--input", required=True, help="Path to the input file")
parser.add_argument("-o", "--output", required=True, help="Path to the output file")
args = parser.parse_args()
input_file_path = args.input
output_file_path = args.output

main_outputs, intermediate_outputs = extract_outputs_from_json(input_file_path)
combined_list = combine_outputs(main_outputs, intermediate_outputs)
quiz_to_csv(combined_list, output_file_path)
