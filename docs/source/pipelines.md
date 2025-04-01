# Pipelines

Janus allows for the configuration and running of pipelines as of version 4.4.0. Pipelines are a series of steps that can be run in sequence. Pipelines are configured in JSON files and can be run with the `janus pipeline` command.

## Configuring a Pipeline

Every pipeline is configured with a JSON file made up of a list of JSON objects. Each object represents a step in the pipeline and can be any number of `Converter`s or `Refiner`s. The list of these objects can be seen below in the [Available Components](#available-components) section.

### Available Components

#### Converters

- [`Aggregator`](autoapi/janus/converter/aggregator/index): Aggregates multiple products into a single output product.
- [`Partitioner`](autoapi/janus/converter/partition/index): Partitions source code in different ways (with an LLM, etc.).
- [`Translator`](autoapi/janus/converter/translate/index): Translates source code from one programming language to another.

#### Evaluators

- [`InlineCommentEvaluator`](autoapi/janus/converter/evaluate/index): Performs an LLM self evaluation on inline comments.
- [`RequirementEvaluator`](autoapi/janus/converter/evaluate/index): Performs an LLM self evaluation on requirements according to INCOSE standards.

#### Documenters

- [`ClozeDocumenter`](autoapi/janus/converter/document/index): Performs cloze commenting on source code.
- [`MultiDocumenter`](autoapi/janus/converter/document/index): Performs multiple documentation tasks on source code.
- [`RequirementsDocumenter`](autoapi/janus/converter/requirements/index): Generates requirements from source code.

### Example Single Stage Pipeline

Every pipeline must have at least one component. The following is an example of a pipeline that uses the `Translator` component to translate from Python to Javascript. The user can also specify some keyword arguments to the component.

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

```bash
janus pipeline --input janus/cli/ --output janus-translation --pipeline pipelines/translate.json --llm my-gpt -l python
```

This is the equivalent to running the following command:

```bash
janus translate --input janus/cli/ --output janus-translation --llm my-gpt --source-language python --target-language javascript
```

### Example Multi Stage Pipeline

[`comment_eval.json`](https://github.com/janus-llm/janus-llm/tree/public/pipelines/comment_eval.json)

```json
[
    {
        "type": "ClozeDocumenter",
        "kwargs": {"comments_per_request": 5}
    },
    {
        "type": "InlineCommentEvaluator",
        "kwargs": {}
    }
]
```

This can then be run with the following command:

```bash
janus pipeline --input janus/cli/ --output janus-translation --pipeline pipelines/comment_eval.json --llm my-gpt -l python
```

This is the equivalent to running the following commands:

```bash
janus document --doc-mode cloze --input janus/cli/ --output janus-translation --llm my-gpt -l python
```

```bash
janus llm-self-eval --input janus-translation --output janus-evals --llm my-gpt -l python -e comments
```

### Using `ConverterPool`s

`ConverterPool`s allow for the parallel execution of multiple `Converter`s.

#### Basic `ConverterPool`

The following is an example of a pipeline that uses a `ConverterPool` to run multiple `Documenter`s in parallel.

```json
[
    {
        "type": "ConverterPool",
        "args": [
            {
                "type": "Documenter",
                "kwargs": {}
            },
            {
                "type": "ClozeDocumenter",
                "kwargs": {"comments_per_request": 5}
            }
        ]
    }
]
```

This runs the `Documenter` and `ClozeDocumenter` in parallel, producing two outputs in the output JSON.


#### `ConverterPool` with Evaluation

The following example runs two `ClozeDocumenter`s in parallel and then runs an `InlineCommentEvaluator` on the output of the `ClozeDocumenter`s.

```json
[
    {
        "type": "ConverterPool",
        "args": [
            {
                "type": "ClozeDocumenter",
                "kwargs": {}
            },
            {
                "type": "ClozeDocumenter",
                "kwargs": {"comments_per_request": 5}
            }
        ]
    },
    {
        "type": "InlineCommentEvaluator",
        "kwargs": {"eval_items_per_request": 5}
    }
]
```

#### `ConverterPool` with `ConverterPassthrough`

The `ConverterPassthrough` component allows for the output of one `Converter` to be passed to the next stage of the pipeline without modification.

```json
[
    {
        "type": "ClozeDocumenter",
        "kwargs": {"comments_per_request": 5}
    },
    {
	"type": "ConverterPool",
	"args": [
	    {
		"type": "InlineCommentEvaluator"
	    },
	    {
		"type": "ConverterPassthrough"
	    }
	]
    }
]
```

In this example, the output of the `ClozeDocumenter` is passed to the `InlineCommentEvaluator` and the `ConverterPassthrough`. This produces two outputs in the output JSON: the output of the `InlineCommentEvaluator` and the output of the `ClozeDocumenter`.


#### `ConverterPool` with Input and Output Labels

Every `Converter` allows for the specification of input and output labels.

```json
[
    {
        "type": "ConverterPool",
        "args": [
            {
                "type": "ClozeDocumenter",
                "kwargs": {"output_label": "dtest"}
            },
            {
                "type": "ClozeDocumenter",
                "kwargs": {}
            },
            {
                "type": "ClozeDocumenter",
                "kwargs": {"output_label": "dtest"}
            }
        ]
    },
    {
        "type": "ConverterPool",
	    "args": [
            {
                "type": "InlineCommentEvaluator",
                "kwargs": {"input_labels": "dtest"}
            }
	    ]
    }
]
```

The labels are used to specify which outputs are passed to which inputs. In this example, the output of the first and third `ClozeDocumenter`s are passed to the `InlineCommentEvaluator`, and the output of the second `ClozeDocumenter` is kept in the intermediate outputs of the resultant JSON file.


#### `ConverterPool` with Input Types

Every `Converter` has an associated `output_type` that informs other `Converters` of the type of output it produces. The `input_types` argument allows for the specification of the types of input that a `Converter` can accept.

```json
[
    {
        "type": "ConverterPool",
        "args": [
            {
                "type": "Documenter",
                "kwargs": {}
            },
            {
                "type": "ClozeDocumenter",
                "kwargs": {"comments_per_request": 5}
            }
        ]
    },
    {
        "type": "ConverterPool",
        "args": [
            {
	            "type": "Translator",
		        "kwargs": {"input_types": "documentation"}
            },
            {
                "type": "InlineCommentEvaluator"
            }
	]
    }
]
```

This example runs a `Documenter` and a `ClozeDocumenter` in parallel, producing two outputs in the output JSON. The outputs are then passed to a `ConverterPool` that runs a `Translator` and an `InlineCommentEvaluator` in parallel. The `Translator` is specified to accept only documentation as input, so it will only accept the output of the `Documenter` and not the `ClozeDocumenter`.

##### Available Output Types

The available output types for each converter are listed here:
- `DiagramGenerator`: `diagram`
- `Documenter`: `documentation`
- `MultiDocumenter`: `multidocumentation`
- `ClozeDocumenter`: `cloze_comments`
- `PseudocodeDocumenter`: `pseudocode`
- `RequirementsDocumenter`: `requirements`
- `Partitioner`: `partition`
- `RequirementEvaluator`: `requirements_eval`
- `InlineCommentEvaluator`: `cloze_comments_eval`
