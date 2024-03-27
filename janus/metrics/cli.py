import typer

evaluate = typer.Typer(
    help="Evaluation of generated source code or documentation against a reference file.",
    add_completion=False,
    no_args_is_help=True,
)
