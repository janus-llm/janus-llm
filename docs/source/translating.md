# Translating

In order to translate from one programming language to another, you'll need to use the `janus translate` subcommand in the CLI. The following instructions will guide you through the process.

First, you need to [add an LLM](quickstart.md) to your configuration.

## Translating Files

You'll need to specify at least the source language and the target language as well as the input directory/file and output directory.

```bash
janus translate --source-language matlab --target-language python --input janus/language/treesitter/_tests/languages --output python-tests --llm my-gpt
```

Or you can specify that you would like to put the result into the Chroma DB:

```bash
janus translate --source-language matlab --target-language python --input janus/language/treesitter/_tests/languages --output python-tests --llm my-gpt --collection my-collection
```
