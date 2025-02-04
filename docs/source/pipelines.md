# Pipelines

Janus allows for the configuration and running of pipelines as of version 4.4.0. Pipelines are a series of steps that can be run in sequence. Pipelines are configured in JSON files and can be run with the `janus pipeline` command.

## Configuring a Pipeline

Every pipeline is configured with a JSON file made up of a list of JSON objects. Each object represents a step in the pipeline and can be any number of `Converter`s or `Refiner`s. The list of these objects can be seen below in the [Available Compoenents](#available-components) section.

### Available Components

#### Converters

- `Aggregator`: Aggregates multiple products into a single output product.
- `Partitioner`: Partitions source code in different ways (with an LLM, etc.).
- `Translator`: Translates source code from one programming language to another.

#### Evaluators

- `InlineCommentEvaluator`: Performs an LLM self evaluation on inline comments.
- `RequirementEvaluator`: Performs an LLM self evaluation on requirements according to INCOSE standards.

#### Documenters

- `ClozeDocumenter`: Performs cloze commenting on source code.
- `MultiDocumenter`: Performs multiple documentation tasks on source code.
- `RequirementsDocumenter`: Generates requirements from source code.

### Example Single Stage Pipeline

Every pipeline must have at least one component. The following is an example of a pipeline that uses the `DiagramGenerator` component to generate a UML diagram from source code. The user can also specify some keyword arguments to the component.

[`translate.json`](https://github.com/janus-llm/janus-llm/tree/public/pipelines/translate.json):

```json
[
    {
        "type": "Translator",
        "kwargs": {"source_language": "python", "target_language": "javascript"}
    }
]
```

This can then be run with the following command:

```shell
janus pipeline --input janus/cli/ --output janus-translation --pipeline janus/pipelines/translate.json --llm my-gpt -l python
```

This is the equivalent to running the following command:

```shell
janus translate --input janus/cli/ --output janus-translation --llm my-gpt --source-language python --target-language javascript
```

