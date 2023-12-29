from pathlib import Path

import click
import typer
from typing_extensions import Annotated

from janus.parsers.code_parser import PARSER_TYPES
from janus.translate import VALID_MODELS, Translator
from janus.utils.enums import LANGUAGES
from janus.utils.logger import create_logger

log = create_logger(__name__)

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


if __name__ == "__main__":
    app()