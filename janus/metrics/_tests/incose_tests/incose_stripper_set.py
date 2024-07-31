import json
import typer

def strip_metadata_for_incose_set(input_data: dict) -> dict:
    """
    Strips out metadata from the input JSON data, retaining only the "code" and "requirements" fields. Formatting for LLM self evaluation for Incose requirments evaluating set of requirments. 
    Example cli: python strip_metadata.py input.json output.json

    Args:
        input_data (dict): The input JSON data.

    Returns:
        dict: The processed JSON data with only the "code" and "requirements" fields.
    """
    output_data = {"output": []}
    
    for item in input_data["output"]:
        filtered_item = {
            "code": item.get("code"),
            "requirements": item.get("requirements")
        }
        output_data["output"].append(filtered_item)
    
    return output_data

def main(input_file: str, output_file: str):
    # Load the input JSON data from a file
    with open(input_file, "r") as infile:
        input_json = json.load(infile)

    # Process the input data
    output_json = strip_metadata_for_incose_set(input_json)

    # Save the processed data to a new file
    with open(output_file, "w") as outfile:
        json.dump(output_json, outfile, indent=4)

    print(f"Metadata stripped and new JSON saved to {output_file}")

if __name__ == "__main__":
    typer.run(main)
