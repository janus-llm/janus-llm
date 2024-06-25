# Translating

In order to translate from one programming language to another, you'll need to use the `janus translate` subcommand in the CLI. The following instructions will guide you through the process.

First, you need to add an LLM to your configuration. You can do this by running the following command:

## Adding an LLM

```shell
janus llm add my-gpt-4 --type OpenAI
```

This will add an LLM configuration file with the name `my-gpt-4`.

Output:

```shell
Model config written to /Users/mdoyle/.janus/llm/my-gpt-4.json
```

You can then modify this JSON file with different hyperparameters.

## Translating Files

You'll need to specify at least the source language and the target language as well as the input directory and output directory.

```shell
janus translate --source-lang matlab --target-lang python --input-dir janus/language/treesitter/_tests/languages --output-dir python-tests
```

This will use the default model (`gpt-3.5-turbo-0125`) to translate the files in the input directory from MATLAB to Python and place the translated files in the output directory.

You can also specify the model we added earlier to use for translation:

```shell
janus translate --source-lang matlab --target-lang python --input-dir janus/language/treesitter/_tests/languages --output-dir python-tests --llm-name my-gpt-4
```

Or you can specify that you would like to put the result into the Chroma DB:

```shell
janus translate --source-lang matlab --target-lang python --input-dir janus/language/treesitter/_tests/languages --output-dir python-tests --llm-name my-gpt-4 --collection my-collection
```

Look to the [Quick Start](quickstart.md) documentation for more information on how to interact with the Chroma DB.
