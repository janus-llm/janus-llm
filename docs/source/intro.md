# Introduction

Janus (`janus-llm`) uses LLMs to transcode libraries from some language to Python.

[GitHub Page](https://github.com/mitrefireline/janus)

## Running the Simulation

### Installing via Pip

```shell
pip install janus-llm
```

### Installing from Source

Clone the repository:

```shell
git clone git@github.com:mitrefireline/janus.git
```

**NOTE**: Make sure you're using Python 3.9, due to PyGame (scheduled to be removed).

Then, install the requirements:

```shell
export POETRY_VERSION=1.4.0
curl -sSkL https://install.python-poetry.org | python -
export PATH=$PATH:$HOME/.local/bin
poetry install --no-dev
```

### Using as a Python Module

TODO
