# Pipelines

Janus allows for the configuration and running of pipelines as of version 4.4.0. Pipelines are a series of steps that can be run in sequence. Pipelines are configured in JSON files and can be run with the `janus pipeline` command.

## Configuring a Pipeline

Every pipeline is configured with a JSON file made up of a list of JSON objects. Each object represents a step in the pipeline and can be any number of `Converter`s or `Refiner`s. The list of these objects can be seen below in the [Available Compoenents](#available-components) section.

### Available Components

#### Converters



### Example Single Stage Pipeline

Every pipeline must have at least one component. The following is an example of a pipeline that uses the `DiagramGenerator` component to generate a UML diagram from source code. The user can also specify some keyword arguments to the component.

[`diagram.json`](https://github.com/janus-llm/janus-llm/tree/public/janus/pipelines/diagram.json):

```json
[
    {
        "type": "DiagramGenerator",
        "kwargs": {}
    }
]
```

This can then be run with the following command:

```shell
janus pipeline --input janus/cli/ --output janus-diagrams --pipeline janus/pipelines/diagram.json --llm my-gpt -l python
```

This is the equivalent to running the following command:

```shell
janus diagram --input janus/cli/ --output janus-diagrams --llm my-gpt -l python
```

