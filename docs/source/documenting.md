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

## Requirement Generation

Requirement generation is a way to generate documentation from source code by extracting requirements.

### Example

```shell
janus document  --doc-mode requirements --input janus/cli/ --output-dir janus-docs --llm my-gpt --language python -r RequirementsFormatRefiner
```

## Output

In the output JSON for `translate.py`, this was the output (trimmed for brevity):

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
