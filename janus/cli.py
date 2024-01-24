import os
from pathlib import Path
from copy import deepcopy

import click
import typer
from typing_extensions import Annotated

from .embedding.collections import Collections
from .embedding.database import ChromaEmbeddingDatabase
from .embedding.vectorize import ChromaDBVectorizer
from .parsers.code_parser import PARSER_TYPES
from .translate import VALID_MODELS, Translator
from .utils.enums import LANGUAGES, CUSTOM_SPLITTERS
from .utils.logger import create_logger
from .language.mumps import MumpsSplitter
from .language.binary import BinarySplitter
from .language.treesitter import TreeSitterSplitter
from .llm import MODEL_CONSTRUCTORS, MODEL_DEFAULT_ARGUMENTS, TOKEN_LIMITS

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
            click_type=click.Choice(sorted(VALID_MODELS)),
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


@app.command(help="Connect to/create a database or print the currently used database.")
def db(
    cmd: Annotated[
        str,
        typer.Argument(
            help=(
                "The command to run. Either 'init' to set the database location or "
                "'status' to print the current location."
            )
        ),
    ],
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
    """Connect to/create a database or print the currently used database

    Arguments:
        cmd: The command to run. Either "init" to set the database location or "status"
            to print the current database location
        path: The path to the database file
        url: The URL of the database
    """
    global db_loc
    if cmd == "init":
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
        # TODO: Create chroma database if it doesn't exist
    elif cmd == "status":
        print(f"Chroma DB currently pointing to {db_loc}")
    else:
        print("Please provide either init or status to db command")


@app.command(help="List the current database's collections.")
def ls() -> None:
    """List the current database's collections"""
    db = ChromaEmbeddingDatabase(db_loc)
    collections = Collections(db)
    print(collections.get())


@app.command(help="Add a collection to the current database.")
def add(
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
    #TODO: import factory
    vectorizer_factory = ChromaDBVectorizer()
    vectorizer = vectorizer_factory.create_vectorizer(
            source_language=input_lang,
            path=db_loc,
    )
    model_arguments = deepcopy(MODEL_DEFAULT_ARGUMENTS[model_name])

    # Load the model
    llm = MODEL_CONSTRUCTORS[model_name](**model_arguments)

    max_tokens = TOKEN_LIMITS.get(model_name, 4096) // 2.5
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

@app.command(help="Remove a collection from the database.")
def remove(
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


if __name__ == "__main__":
    app()
