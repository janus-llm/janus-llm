import argparse
import json
import subprocess
import pandas as pd
from pathlib import Path
import re


def get_line_analysis(output_dir: Path | str) -> pd.DataFrame:
    """
    Run pyright on a given directory and return the results.
    The directory structure must be as follows, with (1) being the top-level
        directory (provided), (2) being its subdirectories, etc.:
        1. Underscore-separated parameter names
        2. Underscore-separated parameter values
        3. Integer iteration number, zero-indexed
        4. Filename matching input
    Examples:
        model_split/gpt-4_minimum/0/PSSBPSUT.py
        model_split/gpt-3.5-turbo-16k_maximum/5/PSS32P5.py
        temp/0.7/2/PSSBPSUT.py
        prompt-id_model_temp/v1.2_gpt-3.5-turbo_0.7/4/PSSJXR5.py
    """
    output_dir = Path(output_dir).expanduser().resolve()

    # Run pyright on the full output directory, returned in JSON format
    result = subprocess.run(
        ["pyright", "--outputjson", str(output_dir)],
        capture_output=True,
        text=True
    )
    result = json.loads(result.stdout)

    # Extract the important information from pyright output
    file, severity, message, start_line, end_line, rule = zip(*(
        (
            Path(m['file']), m['severity'], m['message'],
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

    # Format rules, convert messages to rules where necessary
    line_df['rule'] = line_df.rule.str.replace(r'^report', '', regex=True)
    line_df.loc[
        line_df.message.str.contains('assigned before global declaration'),
        'rule'] = "UndefinedGlobalDeclaration"
    line_df.loc[
        line_df.message.str.contains('No binding for nonlocal'),
        'rule'] = "UndefinedNonlocalDeclaration"
    line_df.loc[
        line_df.message.str.contains('Duplicate parameter'),
        'rule'] = "DuplicateParameterWarning"
    line_df.loc[
        line_df.message.str.contains('f-string'),
        'rule'] = "IllFormattedFStringError"
    line_df.loc[
        line_df.message.str.contains('Too many type arguments'),
        'rule'] = "TooManyTypeArgumentsWarning"
    line_df.loc[
        line_df.rule.isna(), 'rule'] = (
        line_df[line_df.rule.isna()].message
            .replace({
                r'\.': 'period',
                r'[\[\]]': 'square bracket',
                r'[\{\}]': 'curly bracket',
                r'[\(\)]': 'parenthesis',
                r'\:': 'colon',
                r'\=': 'equals',
                r'"\\u24"': 'dollar sign',
                r'"\\u21"': 'exclamation mark',
                r'"\\u3f"': 'question mark'
             }, regex=True)
            .str.title()
            .replace(r'[\s";\-/]', '', regex=True)
    )
    line_df['rule'] = line_df.rule + line_df.severity.str.title()

    return line_df


def get_file_analysis(input_dir: str, output_dir: str) -> pd.DataFrame:
    """
    Run pyright on a given directory and return the results.
    The directory structure must be as follows, with (1) being the top-level
        directory (provided), (2) being its subdirectories, etc.:
        1. Underscore-separated parameter names
        2. Underscore-separated parameter values
        3. Integer iteration number, zero-indexed
        4. Filename matching input
    Examples:
        model_split/gpt-4_minimum/0/PSSBPSUT.py
        model_split/gpt-3.5-turbo-16k_maximum/5/PSS32P5.py
        temp/0.7/2/PSSBPSUT.py
        prompt-id_model_temp/v1.2_gpt-3.5-turbo_0.7/4/PSSJXR5.py
    """
    input_dir = Path(input_dir).expanduser().resolve()
    output_dir = Path(output_dir).expanduser().resolve()
    parameter_names = output_dir.name.split('_')

    # Get length of input and output files
    # Note that input files are indexed only on filename (e.g. PSSBPSUT) while
    #  output files are indexed on full absolute path
    input_file_lengths = pd.Series({
        f.with_suffix('').name: len(f.read_text().split('\n'))
        for f in input_dir.rglob('*.m')
    })
    input_file_routines = pd.Series({
        f.with_suffix('').name: len(re.findall(r"(?:^|\n)\S", f.read_text()))
        for f in input_dir.rglob('*.m')
    })
    output_file_lengths = pd.Series({
        f.resolve(): len(f.read_text().split('\n'))
        for f in output_dir.rglob('*.py')
    })
    output_file_ill_formatted = pd.Series({
        f.resolve(): re.search(r"(?:^|\n)[ \t]*#.*child_", f.read_text()) is not None
        for f in output_dir.rglob('*.py')
    })

    line_df = get_line_analysis(output_dir)

    file_df = output_file_lengths.to_frame('output_lines')

    # Get the total number of errors and warnings per file
    file_df = file_df.merge(
        line_df.groupby(['file', 'severity']).size().unstack(fill_value=0),
        left_index=True,
        right_on='file',
        how='left'
    ).fillna(0).set_index('file')

    # Get the total number of lines of warnings and errors per file
    file_df = file_df.merge(
        line_df.groupby(['file', 'severity']).lines.sum().unstack(fill_value=0),
        left_index=True,
        right_on='file',
        suffixes=('s', '_lines'),
        how='left'
    ).fillna(0).set_index('file')

    # Get the number of warning codes per file (e.g. reportUndefinedVariable)
    file_df = file_df.merge(
        line_df.groupby(['file', 'rule']).size().unstack(fill_value=0),
        left_index=True,
        right_on='file',
        how='left'
    ).fillna(0).set_index('file')

    # Parse filenames to get experiment information
    file_df = file_df.reset_index()
    file_df['file'] = file_df.file.apply(Path)
    file_df['filename'] = file_df.file.apply(lambda p: p.with_suffix('').name)
    file_df['experiment'] = file_df.file.apply(lambda p: p.parent.parent.name)
    file_df[parameter_names] = file_df.experiment.str.split('_', expand=True)
    file_df['iter'] = file_df.file.apply(lambda p: p.parent.name)

    # Add the input and output file lengths for normalization
    file_df = file_df.merge(
        input_file_lengths.rename('input_length'),
        left_on='filename',
        right_index=True
    )
    file_df = file_df.merge(
        input_file_routines.rename('num_routines'),
        left_on='filename',
        right_index=True
    )
    file_df = file_df.merge(
        output_file_lengths.rename('output_length'),
        left_on='file',
        right_index=True
    )
    file_df = file_df.merge(
        output_file_ill_formatted.rename('recombination_error'),
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

    df = get_file_analysis(args.input_dir, args.translated_dir)
    df['input_ratio'] = df.output_length / df.input_length
    df.to_csv(Path(args.translated_dir) / 'error_counts.tsv', sep='\t', index=False)
    g = df.groupby('experiment')
    print(g[['normalized_error_lines', 'normalized_warning_lines']].mean())
    print(g[['normalized_error_lines', 'normalized_warning_lines']].median())
    print(g.input_ratio.mean())
