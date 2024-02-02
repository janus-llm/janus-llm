# Reading Binaries
`janus-llm` uses Ghidra to decompile and parse binary files. This allows the user to translate binaries to another programming language or to perform retrieval augmented generation (RAG) on their decompiled contents.

To read a binary as input, you'll follow the same instructions as in the [Quick Start](quickstart.md) documentation. However, you'll first need to [install Ghidra](https://ghidra-sre.org/InstallationGuide.html).

Then you'll set the `GHIDRA_INSTALL_PATH` environment variable to the location of the Ghidra installation. 

```shell
export GHIDRA_INSTALL_PATH=/Users/mdoyle/programs/ghidra_10.4_PUBLIC
```

After setting the environment variable, you can use the `janus` CLI to read binaries.

## Adding to Chroma

```shell
janus db add --input-dir janus/language/binary/_tests --input-lang binary binary-collection
```

Then we can peek at the collection we just created. You can see in the output that it decompiled the _Hello World_ binary to C-like pseudocode and embedded that document in the embedding database:

```shell
janus db ls --peek binary-collection
```

Output:

```output
Collection: binary-collection
  ID: 04b71a0f-50d8-4061-8775-0b48b575601f
  Metadata: {'date_created': '2024-02-01', 'time_created': '22:50:22.857642'}
  Tenant: default_tenant
  Database: default_database
  Length: 1
  Peeking at first entry:
{
    'ids': ['566265ca-c197-11ee-ab3f-5accbc90a9b9'],
    'embeddings': [0.07846622169017792, 0.06490962952375412, '...'],
    'metadatas': [
        {
            'cost': 0,
            'end_line': 8,
            'hash': -7749008126979110064,
            'original_filename': 'hello.bin',
            'start_line': 1,
            'tokens': 20,
            'type': 'translation_unit'
        }
    ],
    'documents': ['undefined4 entry(void)\n\n{\n  _printf("Hello, World!");\n  return 0;\n}\n\n'],
    'uris': None,
    'data': None
}
```

## Translating

```shell
janus translate --input-lang binary --output-lang python --input-dir janus/language/binary/_tests --output-dir python-tests
```

Then we can `cat` the translated code we just created with ChatGPT:

```shell
cat python-tests/hello.py
```

`python-tests/hello.py`:

```python
def entry():
    print("Hello, World!")
    return 0
```
