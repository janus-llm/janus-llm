"""
Script to split a procssed.json file, with support
for specifying an output directory.

In: Path to processed.json file that have 'experiments' +
 'generated_comment_texts'
Out: 'experiments' as file names, with each 'processed' +
'generated_comment_texts' pair split into json.
"""
import argparse
import json
import os


# Function to create directory if not exists
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# Function to write JSON data to a file
def write_json(file_path, data):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


# Main function to process the input and create files
def process_input(input_file, output_dir):
    # Read the input file
    with open(input_file, "r") as f:
        data = json.load(f)

    # Loop through each ID (e.g., DGJTDEL, DGJXE4, etc.)
    for id, content in data.items():
        processed_string = content.get("processed")

        # Loop through each experiment
        for experiment, experiment_data in content.get("experiments", {}).items():
            generated_comment_texts = experiment_data.get("generated_comment_texts")

            # Prepare the content to write in the new JSON file
            output_data = {
                "processed": processed_string,
                "generated_comment_texts": generated_comment_texts,
            }

            # Create the directory structure for each experiment
            experiment_dir = os.path.join(output_dir, experiment)
            ensure_dir(experiment_dir)

            # Write to the respective file named after the ID
            output_file = os.path.join(experiment_dir, f"{id}.json")
            write_json(output_file, output_data)
            print(f"Written {output_file}")


# Setup argument parser for command line interface
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process input and generate output JSON files by experiments."
    )
    parser.add_argument("input_file", type=str, help="Path to the input JSON file")
    parser.add_argument(
        "output_dir", type=str, help="Directory where output files will be stored"
    )

    args = parser.parse_args()

    process_input(args.input_file, args.output_dir)
