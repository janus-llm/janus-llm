import csv
import json


def extract_outputs_from_json(file_path):
    # Read the JSON file
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Extract the "outputs" field
    main_outputs = data.get("outputs", [])

    # Extract the "outputs" field from "intermediate_outputs"
    intermediate_outputs = []
    if "intermediate_outputs" in data:
        for item in data["intermediate_outputs"]:
            intermediate_outputs.extend(item.get("outputs", []))

    # Convert JSON strings to Python objects
    main_outputs = [json.loads(output) for output in main_outputs]
    intermediate_outputs = [json.loads(output) for output in intermediate_outputs]

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
            "reasoning": None,  # Placeholder for reasoning
            "selected-answer-number": None,  # Placeholder for selected-answer-number
            "grading-result": None,  # Placeholder for grading result
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


def quiz_to_csv(quiz, file_path):
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
        "reasoning",
        "selected-answer-number",
        "grading-result",
    ]

    # Open the file for writing
    with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        # Write the header
        writer.writeheader()

        # Write each row
        for key, entry in quiz.items():
            writer.writerow(entry)


# Filepaths
input_file_path = """/home/fm/itmod/test_docs
                /quiz_taker_outputs/Language Features/converter.json
                """
output_file_path = """/home/fm/itmod/test_docs
                /quiz_grader_outputs/quiz_output_language_features.csv
                """
main_outputs, intermediate_outputs = extract_outputs_from_json(input_file_path)
combined_list = combine_outputs(main_outputs, intermediate_outputs)
quiz_to_csv(combined_list, output_file_path)
