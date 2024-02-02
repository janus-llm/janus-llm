# Translating

In order to translate from one programming language to another, you'll need to use the `janus translate` subcommand in the CLI. The following instructions will guide you through the process.

You'll need to specify at least the source language and the target language as well as the input directory and output directory.

```shell
janus translate --source-lang matlab --target-lang python --input-dir janus/language/treesitter/_tests/languages --output-dir python-tests
```

This will use the default model to translate the files in the input directory from MATLAB to Python and place the translated files in the output directory.

You can also specify the model to use for translation:

```shell
janus translate --source-lang matlab --target-lang python --input-dir janus/language/treesitter/_tests/languages --output-dir python-tests --llm-name gpt-4-1106-preview
```

Or you can specify that you would like to put the result into the Chroma DB:

```shell
janus translate --source-lang matlab --target-lang python --input-dir janus/language/treesitter/_tests/languages --output-dir python-tests --llm-name gpt-4-1106-preview --collection my-collection
```

Look to the [Quick Start](quickstart.md) documentation for more information on how to interact with the Chroma DB.
