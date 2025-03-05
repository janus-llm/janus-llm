# Refiners

Refiners can be used in [pipelines](pipelines.md) to improve the quality of the output. They are used to refine the output of a component, and can be used to fix errors, improve formatting, or add additional information.

## Using Refiners

Refiners can be used in the CLI with the `-r` flag. You can specify multiple refiners in a chain, and they will be run in order. The output of one refiner will be used as the input for the next refiner.

```bash
janus translate --input janus/cli/ --output janus-translation --llm my-gpt -l python -r ReflectionRefiner -r CodeFormatRefiner
```

Refiners can also be used in the [`pipeline`](pipelines.md) command by specifying them in a pipeline configuration file.

```json
[
    {
        "type": "RequirementsDocumenter",
        "kwargs": {"refiner_types": ["RequirementsFormatRefiner"]}
    }
]
```

This will run the `RequirementsFormatRefiner` on the output of the `RequirementsDocumenter`.

## Available Refiners

- [`FormatRefiner`](autoapi/janus/refiners/format/index): Base class for formatting refiners.
- [`CodeFormatRefiner`](autoapi/janus/refiners/format/index): Refines the formatting of source code so that it can be correctly parsed.
- [`RequirementsFormatRefiner`](autoapi/janus/refiners/format/index): Refines the formatting of requirements so that they can be correctly parsed. Recommended for use with generating requirements.

- [`SimpleRetry`](autoapi/janus/refiners/refiner/index): Simple retry refiner that will retry the LLM call a specified number of times.
- [`ReflectionRefiner`](autoapi/janus/refiners/refiner/index): Uses LLM reflection to improve the quality of the output.
- [`RequirementsReflectionRefiner`](autoapi/janus/refiners/refiner/index): Uses LLM reflection to improve the quality of requirements, specifically.
- [`HallucinationRefiner`](autoapi/janus/refiners/refiner/index): Uses LLM reflection to attempt to remove hallucinations from the output.

- [`FixUMLConnectionsRefiner`](autoapi/janus/refiners/refiner/index): Fixes connections in UML diagrams.
