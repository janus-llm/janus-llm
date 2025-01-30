# Translating

In order to translate from one programming language to another, you'll need to use the `janus translate` subcommand in the CLI. The following instructions will guide you through the process.

First, you need to add an LLM to your configuration. You can do this by running the following command:

## Adding an LLM

```shell
janus llm add my-gpt --type OpenAI
```

This will add an LLM configuration file with the name `my-gpt`.

Output:

```shell
Model config written to /Users/mdoyle/.janus/llm/my-gpt.json
```

You can then modify this JSON file with different hyperparameters.

## Translating Files

You'll need to specify at least the source language and the target language as well as the input directory and output directory.

```shell
janus translate --source-language matlab --target-language python --input janus/language/treesitter/_tests/languages --output python-tests --llm my-gpt
```

Or you can specify that you would like to put the result into the Chroma DB:

```shell
janus translate --source-language matlab --target-language python --input janus/language/treesitter/_tests/languages --output python-tests --llm my-gpt --collection my-collection
```
