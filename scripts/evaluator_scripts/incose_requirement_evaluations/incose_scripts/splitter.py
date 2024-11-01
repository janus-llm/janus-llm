import os
import json
import argparse

"""
Script to format requirements for the evaluator, now with support for specifying an output directory
and preserving the file structure of the input directory.

In: Directory to JSON files with multiple 'code' str and 'requirement' array
Out: Same directory structure in the output directory, with individual 'code' + 'requirement' pairs.
"""
def requirement_json_parser(input_dir, output_dir):
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)

                with open(file_path, 'r') as file:
                    data = json.load(file)
                
                relative_path = os.path.relpath(root, input_dir)
                output_path = os.path.join(output_dir, relative_path)
                
                # Ensure output directory structure is the same as input
                os.makedirs(output_path, exist_ok=True)

                for index, entry in enumerate(data.get("output", [])):
                    code = entry.get("code", "")
                    requirements = entry.get("requirements", [])

                    # Keeps the old file name but adds a '_{index}' at the end for each individual `code` + `requirement` pairing
                    new_filename = f"{os.path.splitext(filename)[0]}_{index}.json"
                    new_file_path = os.path.join(output_path, new_filename)

                    new_data = {
                        "code": code,
                        "requirements": requirements
                    }

                    # Save reformatted data in new file
                    with open(new_file_path, 'w') as new_file:
                        json.dump(new_data, new_file, indent=2)

                    print(f"Created: {new_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process JSON files in a directory.')
    parser.add_argument('input_directory', type=str, help='The directory containing JSON files to process')
    parser.add_argument('output_directory', type=str, help='The directory to save processed JSON files with preserved structure')

    args = parser.parse_args()

    requirement_json_parser(args.input_directory, args.output_directory)
