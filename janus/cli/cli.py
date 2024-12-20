import logging

import typer
from rich import print

from janus.cli.aggregate import aggregate
from janus.cli.database import db
from janus.cli.diagram import diagram, render
from janus.cli.document import document
from janus.cli.embedding import embedding
from janus.cli.llm import llm
from janus.cli.partition import partition
from janus.cli.self_eval import llm_self_eval
from janus.cli.translate import translate
from janus.metrics.cli import evaluate
from janus.utils.logger import create_logger

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

log = create_logger(__name__)


app = typer.Typer(
    help=(
        "[bold][dark_orange]Janus[/dark_orange] is a CLI for translating, "
        "documenting, and diagramming code using large language models.[/bold]"
    ),
    add_completion=False,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    rich_markup_mode="rich",
)


def version_callback(value: bool) -> None:
    if value:
        from janus import __version__ as version

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


translate = app.command(
    help="Translate code from one language to another using an LLM.",
    no_args_is_help=True,
)(translate)

document = app.command(
    help="Document input code using an LLM.",
    no_args_is_help=True,
)(document)


aggregate = app.command()(aggregate)


partition = app.command(
    help="Partition input code using an LLM.",
    no_args_is_help=True,
)(partition)

diagram = app.command(
    help="Diagram input code using an LLM.",
    no_args_is_help=True,
)(diagram)


llm_self_eval = app.command(
    help="LLM self evaluation",
    no_args_is_help=True,
)(llm_self_eval)


app.add_typer(db, name="db")
app.add_typer(llm, name="llm")
app.add_typer(evaluate, name="evaluate")
app.add_typer(embedding, name="embedding")


render = app.command()(render)


if __name__ == "__main__":
    app()
