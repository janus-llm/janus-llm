# Documenting

There are four different ways you can create documentation from source code:

1. Cloze Commenting
2. Summary Generation
3. Requirement Generation

## Adding a Model

Before you can generate documentation, you need to add an LLM model to your configuration. You can do this by running the following command:

```shell
janus llm add my-gpt --type OpenAI
```

And then follow the CLI instructions to add the model to your configuration.

## Cloze Commenting

Cloze comments are a way to generate documentation from source code by removing comments that already exist in the source code and replace them with LLM-generated comments.

### Example

```shell
janus document  --doc-mode cloze --input janus/cli/ --output-dir janus-docs --llm my-gpt --language python
```

## Summary Generation

Summary generation is a way to generate documentation from source code by summarizing the source code into a single paragraph.

### Example

```shell
janus document  --doc-mode summary --input janus/cli/ --output-dir janus-docs --llm my-gpt --language python
```

### Output

This is the output JSON for `translate.py` (trimmed for brevity):

```json
{
  "input": "...",
  "metadata": {
    "cost": 0.00717475,
    "processing_time": 4.554493188858032,
    "num_requests": 1,
    "input_tokens": 1465,
    "output_tokens": 286
  },
  "outputs": [
    "This Python code defines a command-line interface (CLI) function `translate` using Typer and Click libraries, which facilitates the translation of source code from one programming language to another. The function is part of a larger system that utilizes a language model to perform the translation, allowing users to specify various options such as the source and target languages, directories for input and output files, and parameters that influence the translation process like the model's temperature and maximum prompts. The function also includes options for handling translation failures, specifying custom splitters and refiners, and controlling whether existing files in the output directory should be overwritten. It is designed to enable flexible and customizable translations, making it suitable for different programming languages and versions, and it can integrate with a database to store translated results if desired.\n\nThe expected initial state includes having a directory (`input_dir`) containing source code files to be translated and specifying the source language (`source_lang`) and target language (`target_lang`). The user also needs to provide the desired output directory (`output_dir`) and possibly other optional parameters to customize the translation process. The terminal state results in translated code files being stored in the specified output directory. Potential exceptions that might arise include a `ValueError` if the output files would overwrite the input files due to overlapping directories and languages, or if invalid parameters are provided. Other issues may occur if directory paths are incorrect or if there are problems with the specified language model."
  ]
}
```

## Requirement Generation

Requirement generation is a way to generate documentation from source code by extracting requirements.

### Example

When generating requirements, you have to specify the `RequirementsFormatRefiner` to ensure the requirements are formatted correctly with an extra call to the LLM:

```shell
janus document  --doc-mode requirements --input janus/cli/ --output-dir janus-docs --llm my-gpt --language python -r RequirementsFormatRefiner
```

### Output

This is the output JSON for `translate.py` (trimmed for brevity):

```json
{
  "input": "...",
  "metadata": {
    "cost": 0.065085,
    "processing_time": 31.34817886352539,
    "num_requests": 2,
    "input_tokens": 5280,
    "output_tokens": 2579
  },
  "outputs": [
    "[[\"The tool must accept an input directory containing the source code files to be translated.\", \"The tool must accept the source programming language of the files in the input directory.\", \"The tool must accept an output directory to store the translated code.\", \"The tool must accept the target programming language for translation.\", \"The tool must accept the custom name of the language model to be used for translation.\", \"The tool must optionally accept a directory to store failure files during translation.\", \"The tool must accept a maximum number of prompts for a single functional block before exiting.\", \"The tool must accept an option to control whether existing files in the output directory should be overwritten.\", \"The tool must accept an option to skip including context information in translation prompts.\", \"The tool must accept a sampling temperature for model configuration.\", \"The tool must accept the name or path of the prompt template directory.\", \"The tool must optionally accept a collection name to store translated results in a Chroma DB collection.\", \"The tool must accept the name of a custom splitter to be used for splitting source code blocks.\", \"The tool must accept a list of refiner types to use in the refinement chain.\", \"The tool must optionally accept the name of a custom retriever to use.\", \"The tool must optionally accept the maximum number of tokens the model should process.\", \"The tool must accept an option to use Janus files as inputs for translation.\", \"The tool must handle large directories of source code files efficiently.\", \"The tool must minimize the translation time through optimized processing.\", \"The tool must provide clear and concise help messages for each CLI option.\", \"The tool must log errors and important events to facilitate debugging and monitoring.\", \"The tool must be compatible with modern operating systems and environments.\", \"The tool must be designed to facilitate easy porting to other programming languages.\", \"The tool must ensure that output files do not overwrite input files.\", \"The tool must handle translation errors gracefully and store relevant failure information.\", \"The system must translate source code files from one programming language to another using a specified language model.\", \"The system must provide various options to customize the translation process, including language selection, model configuration, prompt templates, and failure handling.\", \"The system must support including or skipping context information in translation prompts based on user preference.\", \"The system must support custom refiners and splitters to improve translation quality and handle different source code structures.\", \"The tool must provide a command-line interface with options and help messages for user interaction.\", \"The tool must interface with predefined language models and configurations.\", \"The tool must interact with the file system to read input files and write output files.\", \"The tool must be installable via common package managers for the target programming language.\", \"The tool must comply with relevant software licensing and copyright laws.\", \"The tool must include documentation for installation, usage, and configuration options.\"]]"
  ]
}
```
