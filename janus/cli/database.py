from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from janus.cli.constants import db_loc, janus_dir

db = typer.Typer(
    help="Database commands",
    add_completion=False,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@db.command("init", help="Connect to or create a database.")
def db_init(
    path: Annotated[
        str, typer.Option("--path", "-p", help="The path to the database file.")
    ] = str(janus_dir / "chroma.db"),
    url: Annotated[
        str,
        typer.Option(
            "--url",
            "-u",
            help="The URL of the database if the database is running externally.",
        ),
    ] = "",
) -> None:
    import os

    from rich import print

    from janus.cli.constants import db_file
    from janus.embedding.database import ChromaEmbeddingDatabase

    global db_loc
    if url != "":
        print(f"Pointing to Chroma DB at {url}")
        with open(db_file, "w") as f:
            f.write(url)
        db_loc = url
    else:
        path = os.path.abspath(path)
        print(f"Setting up Chroma DB at {path}")
        with open(db_file, "w") as f:
            f.write(path)
        db_loc = path
    global embedding_db
    embedding_db = ChromaEmbeddingDatabase(db_loc)


@db.command("status", help="Print current database location.")
def db_status():
    from rich import print

    print(f"Chroma DB currently pointing to {db_loc}")


@db.command(
    "ls",
    help="List the current database's collections. Or supply a collection name to list "
    "information about its contents.",
)
def db_ls(
    collection_name: Annotated[
        Optional[str], typer.Argument(help="The name of the collection.")
    ] = None,
    peek: Annotated[
        Optional[int],
        typer.Option("--peek", "-p", help="Peek at N entries for a specific collection."),
    ] = None,
) -> None:
    """List the current database's collections"""
    from rich import print

    from janus.embedding.database import ChromaEmbeddingDatabase

    if peek is not None and collection_name is None:
        print(
            "\n[bold red]Cannot peek at all collections. Please specify a "
            "collection by name.[/bold red]"
        )
        return
    db = ChromaEmbeddingDatabase(db_loc)
    from janus.embedding.collections import Collections

    collections = Collections(db)
    collection_list = collections.get(collection_name)
    for collection in collection_list:
        print(
            f"\n[bold underline]Collection[/bold underline]: "
            f"[bold salmon1]{collection.name}[/bold salmon1]"
        )
        print(f"  ID: {collection.id}")
        print(f"  Metadata: {collection.metadata}")
        print(f"  Tenant: [green]{collection.tenant}[/green]")
        print(f"  Database: [green]{collection.database}[/green]")
        print(f"  Length: {collection.count()}")
        if peek:
            entry = collection.peek(peek)
            entry["embeddings"] = entry["embeddings"][0][:2] + ["..."]
            if peek == 1:
                print("  [bold]Peeking at first entry[/bold]:")
            else:
                print(f"  [bold]Peeking at first {peek} entries[/bold]:")
            print(entry)
        print()


@db.command("add", help="Add a collection to the current database.")
def db_add(
    collection_name: Annotated[str, typer.Argument(help="The name of the collection.")],
    model_name: Annotated[str, typer.Argument(help="The name of the embedding model.")],
    input_dir: Annotated[
        str,
        typer.Option(
            "--input",
            "-i",
            help="The directory containing the source code to be added.",
        ),
    ] = "./",
    input_lang: Annotated[
        str, typer.Option("--language", "-l", help="The language of the source code.")
    ] = "python",
    max_tokens: Annotated[
        int,
        typer.Option(
            "--max-tokens",
            "-m",
            help="The maximum number of tokens for each chunk of input source code.",
        ),
    ] = 4096,
) -> None:
    """Add a collection to the database

    Arguments:
        collection_name: The name of the collection to add
        model_name: The name of the embedding model to use
        input_dir: The directory containing the source code to be added
        input_lang: The language of the source code
        max_tokens: The maximum number of tokens for each chunk of input source code
    """
    # TODO: import factory
    import json
    from pathlib import Path

    from rich.console import Console

    from janus.cli.constants import collections_config_file, get_collections_config
    from janus.embedding.vectorize import ChromaDBVectorizer
    from janus.language.binary import BinarySplitter
    from janus.language.mumps import MumpsSplitter
    from janus.language.naive.registry import CUSTOM_SPLITTERS
    from janus.language.treesitter import TreeSitterSplitter
    from janus.utils.enums import LANGUAGES

    console = Console()

    added_to = _check_collection(collection_name, input_dir)
    collections_config = get_collections_config()

    with console.status(
        f"Adding collection: [bold salmon]{collection_name}[/bold salmon]",
        spinner="arrow3",
    ):
        vectorizer_factory = ChromaDBVectorizer()
        vectorizer = vectorizer_factory.create_vectorizer(
            path=db_loc, config=collections_config
        )
        vectorizer.get_or_create_collection(collection_name, model_name=model_name)
        input_dir = Path(input_dir)
        suffixes = [f".{ext}" for ext in LANGUAGES[input_lang]["suffixes"]]
        input_paths = [file for ext in suffixes for file in input_dir.rglob(f"**/*{ext}")]

        if input_lang in CUSTOM_SPLITTERS:
            if input_lang == "mumps":
                splitter = MumpsSplitter(
                    max_tokens=max_tokens,
                )
            elif input_lang == "binary":
                splitter = BinarySplitter(
                    max_tokens=max_tokens,
                )
        else:
            splitter = TreeSitterSplitter(
                language=input_lang,
                max_tokens=max_tokens,
            )
        for input_path in input_paths:
            input_block = splitter.split(input_path)
            vectorizer.add_nodes_recursively(
                input_block,
                collection_name,
                input_path.name,
            )
    total_files = len(
        [path for path in Path.glob(input_dir, "**/*") if not path.is_dir()]
    )
    if added_to:
        print(
            f"\nAdded to [bold salmon1]{collection_name}[/bold salmon1]:\n"
            f"  Embedding Model: [green]{model_name}[/green]\n"
            f"  Input Directory: {input_dir.absolute()}\n"
            f"  {input_lang} [green]{suffixes}[/green] Files: "
            f"{len(input_paths)}\n"
            "  Other Files (skipped): "
            f"{total_files - len(input_paths)}\n"
        )
    else:
        print(
            f"\nCreated [bold salmon1]{collection_name}[/bold salmon1]:\n"
            f"  Embedding Model: '{model_name}'\n"
            f"  Input Directory: {input_dir.absolute()}\n"
            f"  {input_lang} [green]{suffixes}[/green] Files: "
            f"{len(input_paths)}\n"
            "  Other Files (skipped): "
            f"{total_files - len(input_paths)}\n"
        )
    with open(collections_config_file, "w") as f:
        json.dump(vectorizer.config, f, indent=2)


@db.command(
    "rm",
    help="Remove a collection from the database.",
)
def db_rm(
    collection_name: Annotated[str, typer.Argument(help="The name of the collection.")],
    confirm: Annotated[
        bool,
        typer.Option(
            "--yes",
            "-y",
            help="Confirm the removal of the collection.",
        ),
    ],
) -> None:
    """Remove a collection from the database

    Arguments:
        collection_name: The name of the collection to remove
    """
    from rich.prompt import Confirm

    from janus.embedding.collections import Collections
    from janus.embedding.database import ChromaEmbeddingDatabase

    if not confirm:
        delete = Confirm.ask(
            f"\nAre you sure you want to [bold red]remove[/bold red] "
            f"[bold salmon1]{collection_name}[/bold salmon1]?",
        )
    else:
        delete = True
    if not delete:
        raise typer.Abort()
    db = ChromaEmbeddingDatabase(db_loc)
    collections = Collections(db)
    collections.delete(collection_name)
    print(
        f"[bold red]Removed[/bold red] collection "
        f"[bold salmon1]{collection_name}[/bold salmon1]"
    )


def _check_collection(collection_name: str, input_dir: str | Path) -> bool:
    from chromadb.errors import InvalidCollectionException

    from janus.embedding.collections import Collections
    from janus.embedding.database import ChromaEmbeddingDatabase

    db = ChromaEmbeddingDatabase(db_loc)
    collections = Collections(db)
    added_to = False
    try:
        collections.get(collection_name)
        # confirm_add = Confirm.ask(
        #     f"\nCollection [bold salmon1]{collection_name}[/bold salmon1] exists. Are "
        #     "you sure you want to update it with the contents of"
        #     f"[bold green]{input_dir}[/bold green]?"
        # )
        added_to = True
        # if not confirm_add:
        #     raise typer.Abort()
    except InvalidCollectionException:
        pass
    return added_to
