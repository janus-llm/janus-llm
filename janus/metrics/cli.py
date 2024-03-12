import typer

evaluate = typer.Typer(
    help="Evaluation",
    add_completion=False,
    no_args_is_help=True,
)

state = {}


@evaluate.callback()
def evaluate_main(src_file: str, cmp_file: str, out_file: str):
    state["src_file"] = src_file
    state["cmp_file"] = cmp_file
    state["out_file"] = out_file
