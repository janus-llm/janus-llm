import json
import os
from pathlib import Path

import click
import typer
from typing_extensions import Annotated

from .embedding.collections import Collections
from .embedding.database import ChromaEmbeddingDatabase
from .embedding.vectorize import ChromaDBVectorizer
from .language.binary import BinarySplitter
from .language.mumps import MumpsSplitter
from .language.treesitter import TreeSitterSplitter
from .llm import load_model
from .llm.models_info import (
    COST_PER_MODEL,
    MODEL_CONFIG_DIR,
    MODEL_TYPE_CONSTRUCTORS,
    TOKEN_LIMITS,
)
from .parsers.code_parser import PARSER_TYPES
from .translate import Translator
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


app = typer.Typer(
    help="Choose a command",
    add_completion=False,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)

db = typer.Typer()
llm = typer.Typer()


@app.command(
    help="Translate code from one language to another using an LLM. This will require an "
    "OpenAI API key set to the OPENAI_API_KEY environment variable.",
    no_args_is_help=True,
)
def translate(
    input_dir: Annotated[
        Path,
        typer.Option(
            help="The directory containing the source code to be translated. "
            "The files should all be in one flat directory."
        ),
    ],
    source_lang: Annotated[
        str,
        typer.Option(
            help="The language of the source code.",
            click_type=click.Choice(sorted(LANGUAGES)),
        ),
    ],
    target_lang: Annotated[
        str,
        typer.Option(
            help="The desired output language to translate the source code to.  The "
            "format can follow a 'language-version' syntax.  Use 'text' to get plaintext"
            "results as returned by the LLM.  Examples: python-3.10, mumps, java-10,"
            "text. See source-lang for list of valid target languages."
        ),
    ] = "python-3.10",
    output_dir: Annotated[
        Path,
        typer.Option(help="The directory to store the translated code in"),
    ] = None,
    llm_name: Annotated[
        str,
        typer.Option(
            help="The OpenAI model name to use. See this link for more details:\n"
            "https://platform.openai.com/docs/models/overview",
        ),
    ] = "gpt-3.5-turbo",
    max_prompts: Annotated[
        int,
        typer.Option(
            help="The maximum number of times to prompt a model on one functional block "
            "before exiting the application. This is to prevent wasting too much money."
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
        typer.Option(help="Sampling temperature.", min=0, max=2),
    ] = 0.7,
    prompt_template: Annotated[
        str,
        typer.Option(
            help="Name of the Janus prompt template directory or "
            "path to a directory containing those template files."
        ),
    ] = "simple",
    parser_type: Annotated[
        str,
        typer.Option(
            click_type=click.Choice(sorted(PARSER_TYPES)),
            help="The type of parser to use.",
        ),
    ] = "code",
    collection: Annotated[str, typer.Option("--collection", "-c")] = None,
):
    try:
        target_language, target_version = target_lang.split("-")
    except ValueError:
        target_language = target_lang
        target_version = None
    # make sure not overwriting input
    if source_lang.lower() == target_language.lower() and input_dir == output_dir:
        log.error("Output files would overwrite input! Aborting...")
        exit(-1)

    model_arguments = dict(temperature=temp)
    output_collection = None
    if collection is not None:
        db = ChromaEmbeddingDatabase(db_loc)
        collections = Collections(db)
        output_collection = collections.get_or_create(collection)
    translator = Translator(
        model=llm_name,
        model_arguments=model_arguments,
        source_language=source_lang,
        target_language=target_language,
        target_version=target_version,
        max_prompts=max_prompts,
        prompt_template=prompt_template,
        parser_type=parser_type,
    )
    translator.translate(input_dir, output_dir, overwrite, output_collection)


@db.command("init", help="Connect to/create a database")
def db_init(
    path: Annotated[str, typer.Option(help="The path to the database file.")] = str(
        janus_dir / "chroma.db"
    ),
    url: Annotated[
        str,
        typer.Option(
            help="The URL of the database if the database is running externally."
        ),
    ] = "",
) -> None:
    global db_loc
    if url != "":
        print(f"Setting chroma db to use {url}")
        with open(db_file, "w") as f:
            f.write(url)
        db_loc = url
    else:
        path = os.path.abspath(path)
        print(f"Setting chroma db to use {path}")
        with open(db_file, "w") as f:
            f.write(path)
        db_loc = path
    global embedding_db
    embedding_db = ChromaEmbeddingDatabase(db_loc)


@db.command("status", help="Print current db location")
def db_status():
    print(f"Chroma DB currently pointing to {db_loc}")


@db.command("ls", help="List the current database's collections.")
def db_ls() -> None:
    """List the current database's collections"""
    db = ChromaEmbeddingDatabase(db_loc)
    collections = Collections(db)
    print(collections.get())


@db.command("add", help="Add a collection to the current database.")
def db_add(
    collection_name: Annotated[str, typer.Argument(help="The name of the collection.")],
    input_dir: Annotated[
        str,
        typer.Option(help="The directory containing the source code to be added."),
    ] = "./",
    input_lang: Annotated[
        str, typer.Option(help="The language of the source code.")
    ] = "python",
    model_name: Annotated[
        str, typer.Option(help="The model name to use")
    ] = "gpt-3.5-turbo",
) -> None:
    """Add a collection to the database

    Arguments:
        collection_name: The name of the collection to add
        input_dir: The directory containing the source code to be added
        input_lang: The language of the source code
    """
    # TODO: import factory
    vectorizer_factory = ChromaDBVectorizer()
    vectorizer = vectorizer_factory.create_vectorizer(
        source_language=input_lang,
        path=db_loc,
        model=model_name,
    )

    # Load the model
    llm, token_limit, _ = load_model(model_name)

    max_tokens = token_limit // 2.5
    input_dir = Path(input_dir)
    source_glob = f"**/*.{LANGUAGES[input_lang]['suffix']}"
    input_paths = input_dir.rglob(source_glob)
    if input_lang in CUSTOM_SPLITTERS:
        if input_lang == "mumps":
            splitter = MumpsSplitter(
                max_tokens=max_tokens,
                model=llm,
            )
        elif input_lang == "binary":
            splitter = BinarySplitter(
                max_tokens=max_tokens,
                model=llm,
            )
    else:
        splitter = TreeSitterSplitter(
            language=input_lang,
            max_tokens=max_tokens,
            model=llm,
        )
    for input_path in input_paths:
        input_block = splitter.split(input_path)
        vectorizer._add_nodes_recursively(
            input_block,
            collection_name,
            input_path.name,
        )


@db.command("remove", help="Remove a collection from the database.")
def db_remove(
    collection_name: Annotated[str, typer.Argument(help="The name of the collection.")]
) -> None:
    """Remove a collection from the database

    Arguments:
        collection_name: The name of the collection to remove
    """
    db = ChromaEmbeddingDatabase(db_loc)
    collections = Collections(db)
    print(f"Removing collection {collection_name}")
    collections.delete(collection_name)


@llm.command("add", help="Add a model config to janus")
def llm_add(
    model_name: Annotated[str, typer.Argument(help="The name of the model")],
    type: Annotated[
        str,
        typer.Option(
            help="The type of the model",
            click_type=click.Choice(sorted(list(MODEL_TYPE_CONSTRUCTORS.keys()))),
        ),
    ] = "HuggingFace",
):
    if not MODEL_CONFIG_DIR.exists():
        MODEL_CONFIG_DIR.mkdir(parents=True)
    model_cfg = MODEL_CONFIG_DIR / f"{model_name}.json"
    if type == "HuggingFace":
        url = typer.prompt("Enter the model's url")
        max_tokens = 4096
        max_token_str = typer.prompt("Enter the model's maximum tokens", default=4096)
        if max_token_str != "":
            max_tokens = int(max_token_str)
        in_cost = 0
        in_cost_str = typer.prompt("Enter the cost per input token", default=0)
        if in_cost_str != "":
            in_cost = float(in_cost_str)
        out_cost = 0
        out_cost_str = typer.prompt("Enter the cost per output token", default=0)
        if out_cost_str != "":
            out_cost = float(out_cost_str)
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
            "model_type": type,
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": {"input": in_cost, "output": out_cost},
        }
        with open(model_cfg, "w") as f:
            json.dump(cfg, f)
    elif type == "HuggingFaceLocal":
        pass
    elif type == "OpenAI":
        model_name = typer.prompt("Enter the model name", default="gpt-3.5-turbo")
        params = dict(
            model_name=model_name,
        )
        max_tokens = TOKEN_LIMITS[model_name]
        model_cost = COST_PER_MODEL[model_name]
        cfg = {
            "model_type": type,
            "model_args": params,
            "token_limit": max_tokens,
            "model_cost": model_cost,
        }
        with open(model_cfg, "w") as f:
            json.dump(cfg, f)
    print(f"Model config written to {model_cfg}")


app.add_typer(db, name="db")
app.add_typer(llm, name="llm")


if __name__ == "__main__":
    app()
