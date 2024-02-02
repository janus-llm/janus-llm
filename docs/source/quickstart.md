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

You can check the status of the DB at any time:

```shell
janus db status
```

Then, add a directory of code to the Chroma DB:

```shell
janus db add --input-dir janus --input-lang python janus-collection
```

To look at the collection you just created:

```shell
janus db ls
```

And to peek at the first entry:

```shell
janus db ls janus-collection --peek
```

Output:
```output
Collection: janus-collection
  ID: 2b05d5c4-e459-4019-a57a-f40981d2157d
  Metadata: {'date_created': '2024-02-01', 'time_created': '22:34:29.021953'}
  Tenant: default_tenant
  Database: default_database
  Length: 70
  Peeking at first entry:
{
    'ids': ['1c804356-c195-11ee-802b-5accbc90a9b9'],
    'embeddings': [-0.04940863698720932, -0.05636196956038475, '...'],
    'metadatas': [
        {
            'cost': 0,
            'end_line': 17,
            'hash': -1018617695456695524,
            'original_filename': 'translate.py',
            'start_line': 0,
            'tokens': 163,
            'type': 'merge'
        }
    ],
    'documents': [
        'from copy import deepcopy\nfrom pathlib import Path\nfrom typing import Any, Dict, Set\n\nfrom 
chromadb.api.models.Collection import Collection\nfrom langchain.callbacks import get_openai_callback\n\nfrom 
.converter import Converter, run_if_changed\nfrom .language.block import CodeBlock, TranslatedCodeBlock\nfrom .llm 
import MODEL_CONSTRUCTORS, MODEL_DEFAULT_ARGUMENTS, TOKEN_LIMITS\nfrom .parsers.code_parser import PARSER_TYPES, 
CodeParser, EvaluationParser, JanusParser\nfrom .prompts.prompt import SAME_OUTPUT, TEXT_OUTPUT, PromptEngine\nfrom 
.utils.enums import LANGUAGES\nfrom .utils.logger import create_logger\n\nlog = 
create_logger(__name__)\n\nVALID_MODELS: Set[str] = set(MODEL_CONSTRUCTORS).intersection(MODEL_DEFAULT_ARGUMENTS)'
    ],
    'uris': None,
    'data': None
}
```
