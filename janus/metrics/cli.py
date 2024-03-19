import click
import typer
from typing_extensions import Annotated

from janus.llm import load_model
from janus.metrics.file_pairing import FILE_PAIRING_METHODS
from janus.utils.enums import LANGUAGES

evaluate = typer.Typer(
    help="Evaluation",
    add_completion=False,
    no_args_is_help=True,
)

state = {}


@evaluate.callback()
def evaluate_main(
    src_file: Annotated[str, typer.Option(help)],
    cmp_file: Annotated[str, typer.Option()],
    out_file: Annotated[str, typer.Option()],
    lang: Annotated[
        str,
        typer.Option(
            help="The language of the source code.",
            click_type=click.Choice(sorted(LANGUAGES)),
        ),
    ],
    file_pairing_method: str = typer.Option(
        default="PAIR_BY_FILE", click_type=click.Choice(FILE_PAIRING_METHODS.keys())
    ),
    llm_name: Annotated[
        str,
        typer.Option(
            help="The custom name of the model set with 'janus llm add'.",
        ),
    ] = "gpt-3.5-turbo",
):
    global state
    with open(src_file, "r") as f:
        src = f.read()

    with open(cmp_file, "r") as f:
        cmp = f.read()

    state["src_file"] = src_file
    state["cmp_file"] = cmp_file
    state["out_file"] = out_file
    state["lang"] = lang
    state["llm"], state["token_limit"], state["model_cost"] = load_model(llm_name)
    state["pairs"] = FILE_PAIRING_METHODS[file_pairing_method](src, cmp, state)
