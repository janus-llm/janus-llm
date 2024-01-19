# Introduction

<p align="center">
    <img src="assets/icons/logo_horizontal.png">
</p>

Janus (`janus-llm`) uses LLMs to aid in the modernization of legacy IT systems. The repository can currently do the following:

1. Chunk code of over 100 programming languages to fit within different model context windows.
2. Translate from one programming language to another on a file-by-file basis using an LLM with varying results (with the `translate.py` script).
3. Translate from a binary file to a programming language using Ghidra decompilation.

### Roadmap

**Priorities**

1. A CLI tool, maintaining current functionality.
2. Ability to add chunked code to Chroma Vector DB.
3. Scripts interacting with Chroma Vector DB for RAG translation, requirements generation, and understanding.

### Installing from Source

Clone the repository:

```shell
git clone git@gitlab.mitre.org:it-modernization/team-2/janus.git
```

**NOTE**: Make sure you're using Python 3.10 or 3.11.

Then, install the requirements:

```shell
curl -sSkL https://install.python-poetry.org | python -
export PATH=$PATH:$HOME/.local/bin
poetry install --no-dev
```

### Contributing

See our contributing pages:
* [For MITRE Employees](https://cem-llm.pages.mitre.org/janus/contributing.html#contributing-for-mitre-employees)
