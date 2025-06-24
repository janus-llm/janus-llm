import argparse
import csv
import glob
import json
import os
from pathlib import Path


def extract_outputs_from_json_split(input_file_path, split_index):
    # Read the JSON file
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    main_outputs = None
    intermediate_outputs = None
    # Extract the quiz taker output
    if "output" in data:
        main_outputs = data.get("output", None)
        main_outputs = main_outputs.strip("[]")
        main_outputs = main_outputs.split("][")[split_index]
        main_outputs = f"[{main_outputs}]"
    # Extract the quiz generator output
    if "outputs" in data:
        intermediate_outputs = (
            data["outputs"][split_index].get("input", None).get("output", None)
        )

    # Convert JSON strings to Python objects
    main_outputs = [json.loads(main_outputs)]
    intermediate_outputs = [json.loads(intermediate_outputs)]

    # Flatten lists
    main_outputs = [item for sublist in main_outputs for item in sublist]
    intermediate_outputs = [item for sublist in intermediate_outputs for item in sublist]

    return main_outputs, intermediate_outputs


def extract_outputs_from_json_single(input_file_path, split_index):
    # Read the JSON file
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    main_outputs = None
    intermediate_outputs = None
    # Extract the quiz taker output
    if "output" in data:
        main_outputs = data.get("output", None)
    # Extract the quiz generator output
    if "input" in data and isinstance(data["input"], dict):
        intermediate_outputs = data["input"].get("output", None)

    # Convert JSON strings to Python objects
    main_outputs = [json.loads(main_outputs)]
    intermediate_outputs = [json.loads(intermediate_outputs)]

    # Flatten lists
    main_outputs = [item for sublist in main_outputs for item in sublist]
    intermediate_outputs = [item for sublist in intermediate_outputs for item in sublist]

    return main_outputs, intermediate_outputs


def combine_outputs(main_outputs, intermediate_outputs, split_index):
    # Create a dictionary to map question-id to the combined output
    combined_outputs = {}

    # Populate the dictionary with entries from intermediate_outputs
    for entry in intermediate_outputs:
        question_id = entry["question-id"]
        combined_outputs[question_id] = {
            "split-index": str(split_index),
            "question-id": question_id,
            "question": entry.get("question", ""),
            "option-1": entry.get("option-1", ""),
            "option-2": entry.get("option-2", ""),
            "option-3": entry.get("option-3", ""),
            "option-4": entry.get("option-4", ""),
            "correct-answer-number": entry.get("correct-answer-number", ""),
            "topic": entry.get("topic", ""),
            "selected-answer-number": None,  # Placeholder for number
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


def quiz_to_csv(input_file_path: str | Path, output_file_path: str | Path):
    # Check how many quizzes are in the file
    split_count = 0
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        if "metadata" in data:
            split_count = data["metadata"].get("num_requests", None)

    # Setup the CSV format
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

    # Ensure the file path is a Path object
    output_file_path = Path(output_file_path)
    # Create the directory if it doesn't exist
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    # Check if the file already exists
    if output_file_path.exists():
        # Remove the existing file
        output_file_path.unlink()

    # Open the file for writing
    with open(output_file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write the header
        writer.writeheader()

        if split_count != 1:
            # If the code was split into multiple quizzes
            # loop through each with the split format
            for split_index in range(split_count):
                main_outputs, intermediate_outputs = extract_outputs_from_json_split(
                    input_file_path, split_index
                )
                combined_list = combine_outputs(
                    main_outputs, intermediate_outputs, split_index
                )
                # Write each row
                for _, entry in combined_list.items():
                    writer.writerow(entry)
        else:  # If code was not split, process the single quiz
            main_outputs, intermediate_outputs = extract_outputs_from_json_single(
                input_file_path, 0
            )
            combined_list = combine_outputs(main_outputs, intermediate_outputs, 0)
            # Write each row
            for _, entry in combined_list.items():
                writer.writerow(entry)


# Parse input and output filepath args
parser = argparse.ArgumentParser(description="Process input and output files.")
parser.add_argument(
    "-i", "--input", required=True, help="Path to the input file or directory"
)
parser.add_argument(
    "-o", "--output", required=True, help="Path to the output file or directory"
)
args = parser.parse_args()
input_path = args.input
output_path = args.output

# quiz_to_csv(input_file_path, output_file_path)

# Check if the input is a file or a directory
if os.path.isfile(input_path):
    # If it's a file, process it directly
    quiz_to_csv(input_path, output_path)
elif os.path.isdir(input_path):
    # If it's a directory, loop through all .json files
    json_files = glob.glob(os.path.join(input_path, "*.json"))
    if not json_files:
        print("No .json files found in the directory.")
    for json_file in json_files:
        # Construct output file path for each input file
        output_file = os.path.join(
            output_path, os.path.basename(json_file).replace(".json", ".csv")
        )
        quiz_to_csv(json_file, output_file)
else:
    print("Invalid input path. Please provide a valid file or directory.")
