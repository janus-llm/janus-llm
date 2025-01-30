# Quick Start

Janus LLM (`janus-llm`) allows users to parse and chunk over 100 programming languages and embed that information into a [Chroma](trychroma.com) vector database for retrieval augmented generation (RAG). It also allows the user to directly translate source code from one programming language into another programming language, software requirements, Plant UML, or generate comments.

[GitHub Page](https://github.com/janus-llm/janus-llm)

## Installing

### Installing via Pip

```shell
pip install janus-llm
```

### Installing from Source

Clone the repository:

```shell
git clone git@github.com:janus-llm/janus-llm.git
```

And install the requirements:

**NOTE**: You'll need to have `poetry` installed. If you don't have it, you can install it with `pipx`:

```shell
pipx install poetry
pipx ensurepath
export PATH=$PATH:$HOME/.local/bin
poetry install
```

### Using Janus LLM

With Janus LLM you can:

- [Translate from one programming language to another](translating.md)
- [Create documentation from source code](documenting.md)
- [Generate Plant UML from source code](diagramming.md)
