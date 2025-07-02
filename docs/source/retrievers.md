# Retrievers

Refiners can be used in [pipelines](pipelines.md) to improve the quality of the output. They are used to add additional context, documentation or other relevant sources to your prompt.

## Using Retrievers

Retrievers can be used in the CLI with the `--retriver` flag. You can only specify one retriever per converter

```bash
janus translate --input -i janus/language/treesitter/_tests/languages/ibmhlasm.asm --output janus-translation --llm my-gpt -l ibmhlasm --retriever op_codes
```

Retrievers can also be used in the [`pipeline`](pipelines.md) command by specifying them in a pipeline configuration file.

```json
[
    {
        "type": "RequirementsDocumenter",
        "kwargs": {"retriever_type": "op_codes"}
    }
]
```

This will run the op_codes retriever and insert the result into the context variable of your prompt

## Available Retrievers

- [`ActiveUsingsRetriever`](autoapi/janus/retrievers/retriever/index): Retriever for getting active usings in alc
- [`LanguageDocsRetriever`](autoapi/janus/retrievers/retriever/index): Retrieves information from language docs
- [`OpCodeRetriever`](autoapi/janus/retrievers/alc_retriever/index): Gets op codes and their definitions from predefined json dictionary
