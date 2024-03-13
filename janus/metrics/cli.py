import click
import typer
from typing_extensions import Annotated

from janus.metrics.file_pairing import FILE_PAIRING_METHODS

evaluate = typer.Typer(
    help="Evaluation",
    add_completion=False,
    no_args_is_help=True,
)

state = {}


@evaluate.callback()
def evaluate_main(
    src_file: Annotated[str, typer.Option()],
    cmp_file: Annotated[str, typer.Option()],
    out_file: Annotated[str, typer.Option()],
    file_pairing_method: str = typer.Option(
        default="PAIR_BY_FILE", click_type=click.Choice(FILE_PAIRING_METHODS.keys())
    ),
):
    global state
    with open(src_file, "r") as f:
        src = f.read()

    with open(cmp_file, "r") as f:
        cmp = f.read()

    state["out_file"] = out_file
    state["pairs"] = FILE_PAIRING_METHODS[file_pairing_method](src, cmp)
