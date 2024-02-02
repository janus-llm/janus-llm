# Quick Start

Janus LLM (`janus-llm`) allows users to parse and chunk over 100 programming languages and embed that information into a [Chroma](trychroma.com) vector database for retrieval augmented generation (RAG). It also allows the user to directly translate source code from one language into another using an LLM (results may vary). 

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

Then, install the requirements:

```shell
curl -sSkL https://install.python-poetry.org | python -
export PATH=$PATH:$HOME/.local/bin
poetry install --no-dev
```

## Adding a Directory to a Chroma Collection

First, initialize the `janus` Chroma DB:

```shell
janus db init
```

 
