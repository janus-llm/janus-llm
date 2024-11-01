import os
import json
import argparse

"""Simple script to format requirements to be evaluated using the llm self eval. 

In: Directory to Json file with multiple 'code' str and 'requirement' array
Out: All files in original directory formated for the evaluator split up into individual 'code' + 'requirement' pairs 

"""
def requirement_json_parser(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)

            with open(file_path, 'r') as file:
                data = json.load(file)
            
            for index, entry in enumerate(data.get("output", [])):
                # getting old
                code = entry.get("code", "")
                requirements = entry.get("requirements", [])

                # keeps the  old file name but will add a '_{index}' at the end for each individual `code` + `requirement` pairing: exampleOutput_0.json
                new_filename = f"{os.path.splitext(filename)[0]}_{index}.json"
                new_file_path = os.path.join(directory, new_filename)

                new_data = {
                    "code": code,
                    "requirements": requirements
                }

                # save reformated in new file
                with open(new_file_path, 'w') as new_file:
                    json.dump(new_data, new_file, indent=2)
                
                print(f"Created: {new_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process JSON files in a directory.')
    parser.add_argument('directory', type=str, help='The directory containing JSON files to process')
    
    args = parser.parse_args()

    requirement_json_parser(args.directory)
