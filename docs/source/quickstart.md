# Quick Start

Janus LLM (`janus-llm`) allows users to parse and chunk over 100 programming languages and embed that information into a [Chroma](trychroma.com) vector database for retrieval augmented generation (RAG). It also allows the user to directly translate source code from one programming language into another programming language, software requirements, Plant UML, or generate comments.

[GitHub Page](https://github.com/janus-llm/janus-llm)

## Installing

### Prerequisites

You'll need to install the following prerequisites:

- [gcc](https://gcc.gnu.org/install/) (GNU Compiler Collection) - required for compiling the tree-sitter language parsers.
- [tree-sitter-cli](https://github.com/tree-sitter/tree-sitter/blob/master/cli/README.md) - required for generating the language parsers.

### Installing via pip/poetry/uv

```shell
pip install janus-llm
```

```shell
poetry add janus-llm
```

```shell
uv add janus-llm
```

### Installing from Source

Clone the repository:

```bash
git clone git@github.com:janus-llm/janus-llm.git
```

And install the requirements:

**NOTE**: You'll need to have `poetry` installed. If you don't have it, you can install it with `pipx`:

```bash
pipx install poetry
pipx ensurepath
export PATH=$PATH:$HOME/.local/bin
poetry install
```

### Adding an LLM

```bash
janus llm add myazure
```

This will add an LLM configuration file with the name `myazure`.

Output:

```bash
Model config written to /Users/mdoyle/.janus/llm/myazure.json
```

You can then modify this JSON file with different hyperparameters.

### Using Janus LLM

With Janus LLM you can:

- [Translate from one programming language to another](translating.md)
- [Create documentation from source code](documenting.md)
- [Generate Plant UML from source code](diagramming.md)
- [Use an LLM to evaluate the products that you generate](evaluating.md)
- [Create multi-stage pipelines](pipelines.md)

And most of these will output a standardized JSON file described in more detail [here](janus_json.md).
