from pathlib import Path
import os

import click
import typer
from typing_extensions import Annotated

from janus.parsers.code_parser import PARSER_TYPES
from janus.translate import VALID_MODELS, Translator
from janus.utils.enums import LANGUAGES, EmbeddingType
from janus.utils.logger import create_logger
from janus.embedding.database import ChromaEmbeddingDatabase
from janus.embedding.collections import Collections

log = create_logger(__name__)

homedir = Path.home()

janus_dir = os.path.join(homedir, ".janus")
if not os.path.exists(janus_dir):
    os.mkdir(janus_dir)

db_file = os.path.join(janus_dir, ".db")
if not os.path.exists(db_file):
    with open(db_file, 'w') as f:
        f.write(str(os.path.join(janus_dir, "chroma.db")))

with open(db_file, 'r') as f:
    db_loc = f.read()


app = typer.Typer(
    help="Choose a command",
    add_completion=False,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command(
    help="Translate code from one language to another using LLMs! This will require an "
    "OpenAI API key. Set the OPENAI_API_KEY environment variable to your key",
    no_args_is_help=True,
)
def translate(
    input_dir: Annotated[
        Path,
        typer.Option(
            help="The directory containing the source code to be translated. "
            "The files should all be in one flat directory"
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(help="The directory to store the translated code in"),
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
            "text.  See source-lang for list of valid target languages."
        ),
    ] = "python-3.10",
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
    translator.translate(input_dir, output_dir, overwrite)


@app.command(help="Add source modules to embeddings database")
def add():
    print("TODO")


@app.command(help="Do something else")
def something_else():
    pass

@app.command()
def db(cmd: str, path: str = str(os.path.join(janus_dir, "chroma.db")), url: str = ""):
    global db_loc
    if cmd == "init":
        if url != "":
            print(f"Setting chroma db to use {url}")
            with open(db_file, 'w') as f:
                f.write(url)
            db_loc = url
        else:
            path = os.path.abspath(path)
            print(f"Setting chroma db to use {path}")
            with open(db_file, 'w') as f:
                f.write(path)
            db_loc = path
        global embedding_db
        embedding_db = ChromaEmbeddingDatabase(db_loc)
        #TODO: Create chroma database if it doesn't exist
    elif cmd == "status":
        print(f"Chroma DB currently pointing to {db_loc}")
    else:
        print("Please provide either init or status to db command")

@app.command()
def ls():
    db = ChromaEmbeddingDatabase(db_loc)
    collections = Collections(db)
    print(collections.get())

@app.command()
def add(collection_name: str, input_dir: str = "./", input_lang: str = "python"):
    db = ChromaEmbeddingDatabase(db_loc)
    collections = Collections(db)
    collection = collections.get(EmbeddingType.SOURCE)
    if len(collection) == 0:
        collections.create(EmbeddingType.SOURCE)
        collection = collections.get(EmbeddingType.SOURCE)[0]
    else:
        collection = collection[0]
    suffix = LANGUAGES[input_lang]["suffix"]
    for fname in os.listdir(input_dir):
        if fname.endswith(suffix):
            absolute_path = os.path.abspath(os.path.join(input_dir, fname))
            with open(os.path.join(input_dir, fname), 'r') as f:
                file_contents = f.read()
            collection.upsert(ids=[absolute_path], metadatas=[{"language": input_lang}], documents=[file_contents])


if __name__ == "__main__":
    app()
