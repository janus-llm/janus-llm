# Introduction

<p align="center">
    <img src="assets/icons/logo_horizontal.png">
</p>

Janus (`janus-llm`) uses LLMs to aid in the modernization of legacy IT systems. This could be through the generation of documentation and requirements from source code, or by translating from one language to another.

### Installing via Pip

```shell
pip install janus-llm
```

### Installing from Source

Clone the repository:

```shell
git clone git@github.com:mitrefireline/janus.git
```

**NOTE**: Make sure you're using Python 3.10 or greater.

Then, install the requirements:

```shell
curl -sSkL https://install.python-poetry.org | python -
export PATH=$PATH:$HOME/.local/bin
poetry install --no-dev
```

If you're developing on the project, see our [contributing documentation](https://cem-llm.pages.mitre.org/janus/contributing.html#contributing-for-mitre-employees) for a full development environment setup.

### Using as a Python Module

TODO

### Contributing

See our contributing pages:
* [For MITRE Employees](https://cem-llm.pages.mitre.org/janus/contributing.html#contributing-for-mitre-employees)
* [Open Source](https://mitrefireline.github.io/janus/contributing.html)
