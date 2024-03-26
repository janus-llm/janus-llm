import typer

evaluate = typer.Typer(
    help="Evaluation of generated source code or documentation against a reference file.",
    add_completion=False,
    no_args_is_help=True,
)

# state = {}


# @evaluate.callback()
# def evaluate_main(
#     target: Annotated[
#         str, typer.Option("--target", "-t", help="Target file to evaluate.")
#     ],
#     reference: Annotated[
#         str,
#         typer.Option(
#             "--reference", "-r", help="Reference file to use as reference/baseline."
#         ),
#     ],
#     out_file: Annotated[
#         str, typer.Option("--out-file", "-o", help="Output JSON file to write.")
#     ],
#     language: Annotated[
#         str,
#         typer.Option(
#             "--language",
#             "-l",
#             help="The language of the source code.",
#             click_type=click.Choice(sorted(LANGUAGES)),
#         ),
#     ],
#     file_pairing_method: Annotated[
#         str,
#         typer.Option(
#             "--method",
#             "-m",
#             click_type=click.Choice(FILE_PAIRING_METHODS.keys()),
#             help="Method to use for pairing segments of target and reference files.",
#         ),
#     ] = "file",
#     llm_name: Annotated[
#         str,
#         typer.Option(
#             "--llm",
#             help="The custom name of the model set with 'janus llm add'.",
#         ),
#     ] = "gpt-3.5-turbo",
# ) -> None:
#     """Evaluate the target file against the reference file.

#     Arguments:
#         target: The target file to evaluate.
#         reference: The reference file to use as reference/baseline.
#         out_file: The out file to write.
#         lang: The language of the source code.
#         file_pairing_method: Method to use for pairing segments of target and reference
#             files.
#         llm_name: The custom name of the model set with 'janus llm add'.
#     """
#     global state
#     with open(target, "r") as f:
#         src = f.read()

#     with open(reference, "r") as f:
#         cmp = f.read()

#     state["target_file"] = target
#     state["reference_file"] = reference
#     state["out_file"] = out_file
#     state["lang"] = language
#     state["llm"], state["token_limit"], state["model_cost"] = load_model(llm_name)
#     state["pairs"] = FILE_PAIRING_METHODS[file_pairing_method](src, cmp, state)
