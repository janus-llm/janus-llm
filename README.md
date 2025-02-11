
<p align="center">
    <img src="https://raw.githubusercontent.com/janus-llm/janus-llm/public/assets/icons/logo_horizontal.png">
</p>
<p align="center">
<a href="https://github.com/janus-llm/janus-llm/actions/workflows/pages.yml" target="_blank">
    <img src="https://github.com/janus-llm/janus-llm/actions/workflows/pages.yml/badge.svg" alt="Pages">
</a>
<a href="https://github.com/janus-llm/janus-llm/actions/workflows/publish.yml" target="_blank">
    <img src="https://github.com/janus-llm/janus-llm/actions/workflows/publish.yml/badge.svg" alt="Publish">
</a>
<a href="https://github.com/psf/black" target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style: black">
</a>
<a href="https://pypi.org/project/janus-llm" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/janus-llm" alt="Python versions">
</a>
<a href="https://pypi.org/project/janus-llm" target="_blank">
    <img src="https://img.shields.io/pypi/v/janus-llm?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
</p>

## Overview

Janus (`janus-llm`) uses LLMs to aid in the modernization of legacy IT systems. The repository can currently do the following:

1. Chunk code of over 100 programming languages to fit within different model context windows and add to a [Chroma](https://trychroma.com) vector database.
2. Translate from one programming language to another on a file-by-file basis using an LLM.
3. Translate from a binary file to a programming language using [Ghidra](https://github.com/NationalSecurityAgency/ghidra) decompilation.
4. Generate requirements, UML diagrams, code comments, and summaries from source code.
5. Evaluate the products that you generate.
6. Do 1-5 with a CLI tool (`janus`).


## Installation

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
poetry install
```

### Documentation

See [the documentation](https://janus-llm.github.io/janus-llm) for more information on how to use the package.

### Contributing

See our [contributing pages](https://janus-llm.github.io/janus-llm/contributing.html)

### Copyright
Copyright ©2025 The MITRE Corporation. ALL RIGHTS RESERVED. Approved for Public Release; Distribution Unlimited. Public Release Case Number 23-4084.
