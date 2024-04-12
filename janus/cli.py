import json
import os
from pathlib import Path
from typing import Optional

import click
import typer
from pydantic import AnyHttpUrl
from rich import print
from rich.console import Console
from rich.prompt import Confirm
from typing_extensions import Annotated

from .embedding.collections import Collections
from .embedding.database import ChromaEmbeddingDatabase
from .embedding.embedding_models_info import (
    EMBEDDING_COST_PER_MODEL,
    EMBEDDING_MODEL_CONFIG_DIR,
    EMBEDDING_TOKEN_LIMITS,
    EmbeddingModelType,
)
from .embedding.vectorize import ChromaDBVectorizer
from .language.binary import BinarySplitter
from .language.mumps import MumpsSplitter
from .language.treesitter import TreeSitterSplitter
from .llm.models_info import (
    COST_PER_MODEL,
    MODEL_CONFIG_DIR,
    MODEL_TYPE_CONSTRUCTORS,
    TOKEN_LIMITS,
)
from .metrics.cli import evaluate
from .translate import PARSER_TYPES, Documenter, MadLibsDocumenter, Translator
from .utils.enums import CUSTOM_SPLITTERS, LANGUAGES
from .utils.logger import create_logger

log = create_logger(__name__)
homedir = Path.home().expanduser()

janus_dir = homedir / ".janus"
if not janus_dir.exists():
    janus_dir.mkdir(parents=True)

db_file = janus_dir / ".db"
if not db_file.exists():
    with open(db_file, "w") as f:
        f.write(str(janus_dir / "chroma.db"))

with open(db_file, "r") as f:
    db_loc = f.read()

collections_config_file = Path(db_loc) / "collections.json"


def get_collections_config():
    if collections_config_file.exists():
        with open(collections_config_file, "r") as f:
            config = json.load(f)
    else:
        config = {}
    return config


app = typer.Typer(
    help="Choose a command",
    add_completion=False,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


db = typer.Typer(
    help="Database commands",
    add_completion=False,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
llm = typer.Typer(
    help="LLM commands",
    add_completion=False,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

embedding = typer.Typer(
    help="Embedding model commands",
    add_completion=False,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


def version_callback(value: bool) -> None:
    if value:
        from . import __version__ as version

        print(f"Janus CLI [blue]v{version}[/blue]")
        raise typer.Exit()


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        help="Print the version and exit.",
    ),
) -> None:
    """A function for getting the app version

    This will call the version_callback function to print the version and exit.

    Arguments:
        ctx: The typer context
        version: A boolean flag for the version
    """
    pass


@app.command(
    help="Translate code from one language to another using an LLM.",
    no_args_is_help=True,
)
def translate(
    input_dir: Annotated[
        Path,
        typer.Option(
            "--input",
            "-i",
            help="The directory containing the source code to be translated. "
            "The files should all be in one flat directory.",
        ),
    ],
    source_lang: Annotated[
        str,
        typer.Option(
            "--source-language",
            "-s",
            help="The language of the source code.",
            click_type=click.Choice(sorted(LANGUAGES)),
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output", "-o", help="The directory to store the translated code in."
        ),
    ],
    target_lang: Annotated[
        str,
        typer.Option(
            "--target-language",
            "-t",
            help="The desired output language to translate the source code to. The "
            "format can follow a 'language-version' syntax.  Use 'text' to get plaintext"
            "results as returned by the LLM. Examples: `python-3.10`, `mumps`, `java-10`,"
            "text.",
        ),
    ],
    llm_name: Annotated[
        str,
        typer.Option(
            "--llm",
            "-L",
            help="The custom name of the model set with 'janus llm add'.",
        ),
    ] = "gpt-3.5-turbo",
    max_prompts: Annotated[
        int,
        typer.Option(
            "--max-prompts",
            "-m",
            help="The maximum number of times to prompt a model on one functional block "
            "before exiting the application. This is to prevent wasting too much money.",
        ),
    ] = 10,
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite/--preserve",
            help="Whether to overwrite existing files in the output directory",
        ),
    ] = False,
    temp: Annotated[
        float,
        typer.Option("--temperature", "-T", help="Sampling temperature.", min=0, max=2),
    ] = 0.7,
    prompt_template: Annotated[
        str,
        typer.Option(
            "--prompt-template",
            "-p",
            help="Name of the Janus prompt template directory or "
            "path to a directory containing those template files.",
        ),
    ] = "simple",
    parser_type: Annotated[
        str,
        typer.Option(
            "--parser",
            "-P",
            click_type=click.Choice(sorted(PARSER_TYPES)),
            help="The type of parser to use.",
        ),
    ] = "code",
    collection: Annotated[
        str,
        typer.Option(
            "--collection",
            "-c",
            help="If set, will put the translated result into a Chroma DB "
            "collection with the name provided.",
        ),
    ] = None,
):
    try:
        target_language, target_version = target_lang.split("-")
    except ValueError:
        target_language = target_lang
        target_version = None
    # make sure not overwriting input
    if source_lang.lower() == target_language.lower() and input_dir == output_dir:
        log.error("Output files would overwrite input! Aborting...")
        raise ValueError

    model_arguments = dict(temperature=temp)
    collections_config = get_collections_config()
    translator = Translator(
        model=llm_name,
        model_arguments=model_arguments,
        source_language=source_lang,
        target_language=target_language,
        target_version=target_version,
        max_prompts=max_prompts,
        prompt_template=prompt_template,
        parser_type=parser_type,
        db_path=db_loc,
        db_config=collections_config,
    )
    translator.translate(input_dir, output_dir, overwrite, collection)


@app.command(
    help="Document input code using an LLM.",
    no_args_is_help=True,
)
def document(
    input_dir: Annotated[
        Path,
        typer.Option(
            "--input",
            "-i",
            help="The directory containing the source code to be translated. "
            "The files should all be in one flat directory.",
        ),
    ],
    language: Annotated[
        str,
        typer.Option(
            "--language",
            "-l",
            help="The language of the source code.",
            click_type=click.Choice(sorted(LANGUAGES)),
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir", "-o", help="The directory to store the translated code in."
        ),
    ],
    llm_name: Annotated[
        str,
        typer.Option(
            "--llm",
            "-L",
            help="The custom name of the model set with 'janus llm add'.",
        ),
    ] = "gpt-3.5-turbo",
    max_prompts: Annotated[
        int,
        typer.Option(
            "--max-prompts",
            "-m",
            help="The maximum number of times to prompt a model on one functional block "
            "before exiting the application. This is to prevent wasting too much money.",
        ),
    ] = 10,
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite/--preserve",
            help="Whether to overwrite existing files in the output directory",
        ),
    ] = False,
    doc_mode: Annotated[
        str,
        typer.Option(
            "--doc-mode",
            "-d",
            help="The documentation mode.",
            click_type=click.Choice(["module", "madlibs"]),
        ),
    ] = "madlibs",
    drop_comments: Annotated[
        bool,
        typer.Option(
            "--drop-comments/--keep-comments",
            help="Whether to drop or keep comments in the code sent to the LLM",
        ),
    ] = False,
    temperature: Annotated[
        float,
        typer.Option("--temperature", "-t", help="Sampling temperature.", min=0, max=2),
    ] = 0.7,
    collection: Annotated[
        str,
        typer.Option(
            "--collection",
            "-c",
            help="If set, will put the translated result into a Chroma DB "
            "collection with the name provided.",
        ),
    ] = None,
):
    model_arguments = dict(temperature=temperature)
    collections_config = get_collections_config()
    if doc_mode == "module":
        documenter = Documenter(
            model=llm_name,
            model_arguments=model_arguments,
            source_language=language,
            max_prompts=max_prompts,
            db_path=db_loc,
            db_config=collections_config,
            drop_comments=drop_comments,
        )
    elif doc_mode == "madlibs":
        documenter = MadLibsDocumenter(
            model=llm_name,
            model_arguments=model_arguments,
            source_language=language,
            max_prompts=max_prompts,
            db_path=db_loc,
            db_config=collections_config,
        )

    documenter.translate(input_dir, output_dir, overwrite, collection)


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
    if peek is not None and collection_name is None:
        print(
            "\n[bold red]Cannot peek at all collections. Please specify a "
            "collection by name.[/bold red]"
        )
        return
    db = ChromaEmbeddingDatabase(db_loc)
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
        suffix = LANGUAGES[input_lang]["suffix"]
        source_glob = f"**/*.{suffix}"
        input_paths = [p for p in input_dir.rglob(source_glob)]
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
    total_files = len([p for p in Path.glob(input_dir, "**/*") if not p.is_dir()])
    if added_to:
        print(
            f"\nAdded to [bold salmon1]{collection_name}[/bold salmon1]:\n"
            f"  Embedding Model: [green]{model_name}[/green]\n"
            f"  Input Directory: {input_dir.absolute()}\n"
            f"  {input_lang.capitalize()} [green]*.{suffix}[/green] Files: "
            f"{len(input_paths)}\n"
            "  Other Files (skipped): "
            f"{total_files - len(input_paths)}\n"
        )
        [p for p in Path.glob(input_dir, f"**/*.{suffix}") if not p.is_dir()]
    else:
        print(
            f"\nCreated [bold salmon1]{collection_name}[/bold salmon1]:\n"
            f"  Embedding Model: '{model_name}'\n"
            f"  Input Directory: {input_dir.absolute()}\n"
            f"  {input_lang.capitalize()} [green]*.{suffix}[/green] Files: "
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
    except ValueError:
        pass
    return added_to


@llm.command("add", help="Add a model config to janus")
def llm_add(
    model_name: Annotated[
        str, typer.Argument(help="The user's custom name of the model")
    ],
    model_type: Annotated[
        str,
        typer.Option(
            "--type",
            "-t",
            help="The type of the model",
            click_type=click.Choice(sorted(list(MODEL_TYPE_CONSTRUCTORS.keys()))),
        ),
    ] = "OpenAI",
):
    if not MODEL_CONFIG_DIR.exists():
        MODEL_CONFIG_DIR.mkdir(parents=True)
    model_cfg = MODEL_CONFIG_DIR / f"{model_name}.json"
    if model_type == "HuggingFace":
        url = typer.prompt("Enter the model's URL")
        max_tokens = typer.prompt(
            "Enter the model's maximum tokens", default=4096, type=int
        )
        in_cost = typer.prompt("Enter the cost per input token", default=0, type=float)
        out_cost = typer.prompt("Enter the cost per output token", default=0, type=float)
        params = dict(
            inference_server_url=url,
            max_new_tokens=max_tokens,
            top_k=10,
            top_p=0.95,
            typical_p=0.95,
            temperature=0.01,
            repetition_penalty=1.03,
            timeout=240,
        )
        cfg = {
            "model_type": model_type,
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": {"input": in_cost, "output": out_cost},
        }
    elif model_type == "HuggingFaceLocal":
        model_id = typer.prompt("Enter the model ID")
        task = typer.prompt("Enter the task")
        max_tokens = typer.prompt(
            "Enter the model's maximum tokens", default=4096, type=int
        )
        in_cost = 0
        out_cost = 0
        params = {"model_id": model_id, "task": task}
        cfg = {
            "model_type": model_type,
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": {"input": in_cost, "output": out_cost},
        }
    elif model_type == "OpenAI":
        model_name = typer.prompt("Enter the model name", default="gpt-3.5-turbo")
        params = dict(
            model_name=model_name,
            temperature=0.7,
            n=1,
        )
        max_tokens = TOKEN_LIMITS[model_name]
        model_cost = COST_PER_MODEL[model_name]
        cfg = {
            "model_type": model_type,
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": model_cost,
        }
    else:
        raise ValueError(f"Unknown model type {model_type}")
    with open(model_cfg, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Model config written to {model_cfg}")


@embedding.command("add", help="Add an embedding model config to janus")
def embedding_add(
    model_name: Annotated[
        str, typer.Argument(help="The user's custom name for the model")
    ],
    model_type: Annotated[
        str,
        typer.Option(
            "--type",
            "-t",
            help="The type of the model",
            click_type=click.Choice(list(val.value for val in EmbeddingModelType)),
        ),
    ] = "OpenAI",
):
    if not EMBEDDING_MODEL_CONFIG_DIR.exists():
        EMBEDDING_MODEL_CONFIG_DIR.mkdir(parents=True)
    model_cfg = EMBEDDING_MODEL_CONFIG_DIR / f"{model_name}.json"
    if model_type in EmbeddingModelType.HuggingFaceInferenceAPI.values:
        hf = typer.style("HuggingFaceInferenceAPI", fg="yellow")
        url = typer.prompt(f"Enter the {hf} model's URL", type=str, value_proc=AnyHttpUrl)
        api_model_name = typer.prompt("Enter the model's name", type=str, default="")
        api_key = typer.prompt("Enter the API key", type=str, default="")
        max_tokens = typer.prompt(
            "Enter the model's maximum tokens", default=8191, type=int
        )
        in_cost = typer.prompt("Enter the cost per input token", default=0, type=float)
        out_cost = typer.prompt("Enter the cost per output token", default=0, type=float)
        params = dict(
            model_name=api_model_name,
            api_key=api_key,
        )
        cfg = {
            "model_type": model_type,
            "model_identifier": str(url),
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": {"input": in_cost, "output": out_cost},
        }
    elif model_type in EmbeddingModelType.HuggingFaceLocal.values:
        hf = typer.style("HuggingFace", fg="yellow")
        model_id = typer.prompt(
            f"Enter the {hf} model ID", default="all-MiniLM-L6-v2", type=str
        )
        cache_folder = typer.prompt(
            "Enter the model's cache folder",
            default=EMBEDDING_MODEL_CONFIG_DIR / "cache",
            type=str,
        )
        max_tokens = typer.prompt(
            "Enter the model's maximum tokens", default=8191, type=int
        )
        params = dict(
            cache_folder=str(cache_folder),
        )
        cfg = {
            "model_type": model_type,
            "model_identifier": model_id,
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": {"input": 0, "output": 0},
        }
    elif model_type in EmbeddingModelType.OpenAI.values:
        available_models = list(EMBEDDING_COST_PER_MODEL.keys())

        open_ai = typer.style("OpenAI", fg="green")
        prompt = f"Enter the {open_ai} model name"

        model_name = typer.prompt(
            prompt,
            default="text-embedding-3-small",
            type=click.types.Choice(available_models),
            show_choices=False,
        )
        params = dict(
            model_name=model_name,
            temperature=0.7,
            n=1,
        )
        max_tokens = EMBEDDING_TOKEN_LIMITS[model_name]
        model_cost = EMBEDDING_COST_PER_MODEL[model_name]
        cfg = {
            "model_type": model_type,
            "model_identifier": model_name,
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": model_cost,
        }
    else:
        raise ValueError(f"Unknown model type {model_type}")
    with open(model_cfg, "w") as f:
        json.dump(cfg, f, indent=2)
    print(f"Model config written to {model_cfg}")


app.add_typer(db, name="db")
app.add_typer(llm, name="llm")
app.add_typer(evaluate, name="evaluate")
app.add_typer(embedding, name="embedding")


if __name__ == "__main__":
    app()
