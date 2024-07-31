import json
import typer
from typing import List, Dict, Any

def split_requirements_for_incose_individual(input_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Splits requirements into individual entries, each paired with the associated code. Formatting for LLM self evaluation for Incose requirments evaluating individual requirments. 
    Example cli: python strip_metadata.py input.json output.json

    Args:
        input_data (dict): The input JSON data.

    Returns:
        dict: The processed JSON data with individual requirements paired with their corresponding code.
    """
    output_data = {"output": []}
    
    for item in input_data["output"]:
        code = item.get("code")
        requirements = item.get("requirements", [])
        
        for req_group in requirements:
            for requirement in req_group:
                output_data["output"].append({
                    "code": code,
                    "requirement": requirement
                })
    
    return output_data

def main(input_file: str, output_file: str):
    # Load the input JSON data from a file
    with open(input_file, "r") as infile:
        input_json = json.load(infile)

    # Process the input data
    output_json = split_requirements_for_incose_individual(input_json)

    # Save the processed data to a new file
    with open(output_file, "w") as outfile:
        json.dump(output_json, outfile, indent=4)

    print(f"Metadata stripped and new JSON saved to {output_file}")

if __name__ == "__main__":
    typer.run(main)
