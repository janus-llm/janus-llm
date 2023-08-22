import argparse
import json
import os
import subprocess


def run_pyright_on_file(file_path):
    """
    Run pyright on a given file and return the results.
    """
    result = subprocess.run(["pyright", file_path], capture_output=True, text=True)
    return result.stdout


def extract_errors_and_warnings(output):
    """
    Extract errors and warnings from pyright's output.
    """
    lines = output.split("\n")
    errors = []
    warnings = []

    for line in lines[:-2]:
        if "error" in line:
            errors.append(line)
        elif "warning" in line:
            warnings.append(line)
    return errors, warnings


def main(directory_path, output_file):
    """
    Iterate through the directory, run pyright on each file, and save the
    results in a JSON file.
    """
    results = []

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                output = run_pyright_on_file(file_path)
                errors, warnings = extract_errors_and_warnings(output)
                results.append(
                    {
                        "file": file_path,
                        "total_errors": len(errors),
                        "total_warnings": len(warnings),
                        "errors": errors,
                        "warnings": warnings,
                    }
                )

    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run pyright on a directory and save results to a JSON file."
    )
    parser.add_argument("directory", type=str, help="Directory to check with pyright.")
    parser.add_argument("output_file", type=str, help="Path to save the JSON results.")
    args = parser.parse_args()
    main(args.directory, args.output_file)
