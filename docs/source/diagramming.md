# Diagramming

With Janus LLM you can generate Plant UML from source code. This is useful for generating diagrams from source code, such as class diagrams, sequence diagrams, and activity diagrams.

## Generating Diagrams

To generate diagrams from source code, you'll need to use the `janus diagram` subcommand in the CLI. The following instructions will guide you through the process.

### Adding an LLM

```bash
janus llm add my-gpt --type OpenAI
```

This will add an LLM configuration file with the name `my-gpt`.

Output:

```bash
Model config written to /Users/mdoyle/.janus/llm/my-gpt.json
```

You can then modify this JSON file with different hyperparameters.

### Running the Diagram Command

```bash
janus diagram --input janus/language/treesitter/_tests/languages --output diagrams --llm my-gpt --language python --diagram-type Activity
```

The options for type of diagram are `Class`, `Sequence`, and `Activity`.

You can also specify some [refiners](refiners.md) in a chain to improve the quality of the diagram:

```bash
janus diagram --input janus/language/treesitter/_tests/languages --output diagrams --llm my-gpt --language python --diagram-type Activity -r ReflectionRefiner -r CodeFormatRefiner -r FixParserExceptions
```

This should output a [Janus JSON](janus_json.md) file that then can be used to render the diagram.

## Rendering Diagrams

### Installing PlantUML

There is a script in the Janus LLM repo that will install PlantUML for you. You can run the following command to install it:

```bash
curl https://raw.githubusercontent.com/janus-llm/janus-llm/refs/heads/public/scripts/install_plantuml.sh | bash
```

### Rendering the Diagram

```bash
janus render --input diagrams --output diagrams
```
