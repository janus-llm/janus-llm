import argparse
import json
import os
import subprocess
from collections import defaultdict
import pandas as pd
from pathlib import Path


def analyze_dir(input_directory: str, output_directory: str) -> pd.DataFrame:
    """
    Run pyright on a given file and return the results.
    """
    # Get length of input and output files
    # Note that input files are indexed only on filename (e.g. PSSBPSUT) while
    #  output files are indexed on full absolute path
    input_file_lengths = pd.Series({
        f.with_suffix('').name: len(f.read_text().split('\n'))
        for f in Path(input_directory).iterdir()
    })
    output_file_lengths = pd.Series({
        f.absolute(): len(f.read_text().split('\n'))
        for f in Path(output_directory).rglob('*')
        if f.is_file()
    })

    # Run pyright on the full output directory, returned in JSON format
    result = subprocess.run(
        ["pyright", "--outputjson", output_directory],
        capture_output=True,
        text=True
    )
    result = json.loads(result.stdout)

    # Extract the important information from pyright output
    file, severity, message, start_line, end_line, rule = zip(*(
        (
            m['file'], m['severity'], m['message'],
            m['range']['start']['line'],
            m['range']['end']['line'],
            m['rule'] if 'rule' in m else None
        )
        for m in result['generalDiagnostics']
    ))

    # Create a dataframe, where each row is an individual warning or error
    line_df = pd.DataFrame(dict(
        file=file,
        severity=severity,
        message=message,
        start_line=start_line,
        end_line=end_line,
        rule=rule))

    # Some errors span multiple lines
    line_df['lines'] = line_df.end_line - line_df.start_line + 1

    # Get the total number of errors and warnings per file
    file_df = line_df.groupby(['file', 'severity']).size().unstack(fill_value=0)

    # Get the total number of lines of warnings and errors per file
    file_df = file_df.merge(
        line_df.groupby(['file', 'severity']).lines.sum().unstack(fill_value=0),
        left_index=True,
        right_index=True,
        suffixes=['s', '_lines']
    )

    # Get the number of warning codes per file (e.g. reportUndefinedVariable)
    file_df = file_df.merge(
        line_df.groupby(['file', 'rule']).size().unstack(fill_value=0),
        left_index=True,
        right_index=True
    )

    # Parse filenames to get experiment information
    file_df = file_df.reset_index()
    file_df['file'] = file_df.file.apply(Path)
    file_df['filename'] = file_df.file.apply(lambda p: p.with_suffix('').name)
    experiment_name = file_df.file.apply(lambda p: p.parent.parent.name)
    file_df[['model', 'split']] = experiment_name.str.split('_', expand=True)
    file_df['split'] = file_df.split == 'split'
    file_df['iter'] = file_df.file.apply(lambda p: p.parent.name)

    # Add the input and output file lengths for normalization
    file_df = file_df.merge(
        input_file_lengths.rename('input_length'),
        left_on='filename',
        right_index=True
    )
    file_df = file_df.merge(
        output_file_lengths.rename('output_length'),
        left_on='file',
        right_index=True
    )
    file_df['normalized_error_lines'] = file_df.error_lines / file_df.input_length
    file_df['normalized_warning_lines'] = file_df.warning_lines / file_df.input_length
    return file_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run pyright on a directory and save results to a JSON file."
    )
    parser.add_argument(
        "input_dir",
        type=str,
        help="Directory containing untranslated input files.")
    parser.add_argument(
        "translated_dir",
        type=str,
        help="Directory containing translated python.")
    args = parser.parse_args()

    df = analyze_dir(args.input_dir, args.translated_dir)
    print(df.groupby(['model', 'split'])[['normalized_error_lines', 'normalized_warning_lines']].mean())
