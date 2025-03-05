# Diagramming

With Janus LLM you can generate Plant UML from source code. This is useful for generating diagrams from source code, such as class diagrams, sequence diagrams, and activity diagrams.

## Generating Diagrams

To generate diagrams from source code, you'll need to use the `janus diagram` subcommand in the CLI. The following instructions will guide you through the process.

### Adding a Model

Before you can generate diagrams, you need to [add an LLM](quickstart.md) to your configuration.

### Running the Diagram Command

```bash
janus diagram --input janus/language/treesitter/_tests/languages --output diagrams --llm my-gpt --language matlab --diagram-type Activity
```

The options for type of diagram are `Class`, `Sequence`, and `Activity`.

You can also specify some [refiners](refiners.md) in a chain to improve the quality of the diagram:

```bash
janus diagram --input janus/language/treesitter/_tests/languages --output diagrams --llm my-gpt --language matlab --diagram-type Activity -r ReflectionRefiner -r CodeFormatRefiner -r FixParserExceptions
```

This should output a [Janus JSON](janus_json.md) file that then can be used to render the diagram.

## Rendering Diagrams

### Installing PlantUML

There is a script in the Janus LLM repo that will install PlantUML for you. You can run the following command to install it:

```bash
curl https://raw.githubusercontent.com/janus-llm/janus-llm/refs/heads/public/scripts/install_plantuml.sh | bash
```

### Installing Java

Rendering the diagrams requires Java. [Download](https://www.oracle.com/java/technologies/downloads/) and install the latest JDK to render PlantUML diagrams.

### Rendering the Diagram

```bash
janus render --input diagrams --output diagrams
```
