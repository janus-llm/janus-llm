import inspect
import json
from typing import Callable

import click
import typer
from typing_extensions import Annotated

from janus.llm import load_model
from janus.utils.enums import LANGUAGES

from .cli import evaluate
from .file_pairing import FILE_PAIRING_METHODS
from .splitting import SPLITTING_METHODS


def metric(
    name: None | str = None, help: None | str = None, use_reference: bool = True
) -> Callable:
    """Returns a decorator to add a given metric to the cli

    Metrics must follow the format (src_str, cmp_str, **other_params)

    Arguments:
        name: The name of the metric. If None, the function name is used.
        help: The help text for the metric.

    Returns:
        The decorator function.
    """

    def decorator(function):
        if use_reference:

            def func(
                target: Annotated[
                    str, typer.Option("--target", "-t", help="Target file to evaluate.")
                ],
                reference: Annotated[
                    str,
                    typer.Option(
                        "--reference",
                        "-r",
                        help="Reference file to use as reference/baseline.",
                    ),
                ],
                out_file: Annotated[
                    str,
                    typer.Option("--out-file", "-o", help="Output JSON file to write."),
                ],
                language: Annotated[
                    str,
                    typer.Option(
                        "--language",
                        "-l",
                        help="The language of the source code.",
                        click_type=click.Choice(sorted(LANGUAGES)),
                    ),
                ],
                file_pairing_method: Annotated[
                    str,
                    typer.Option(
                        "--method",
                        "-m",
                        click_type=click.Choice(FILE_PAIRING_METHODS.keys()),
                        help="Method to use for pairing\
                              segments of target and reference files.",
                    ),
                ] = "file",
                llm_name: Annotated[
                    str,
                    typer.Option(
                        "--llm",
                        help="The custom name of the model set with 'janus llm add'.",
                    ),
                ] = "gpt-3.5-turbo",
                *args,
                **kwargs,
            ):
                out = []
                with open(target, "r") as f:
                    target_contents = f.read()

                with open(reference, "r") as f:
                    reference_contents = f.read()
                llm, token_limit, model_cost = load_model(llm_name)
                pairs = FILE_PAIRING_METHODS[file_pairing_method](
                    target_contents,
                    reference_contents,
                    target_file=target,
                    reference_file=reference,
                    out_file=out_file,
                    lang=language,
                    llm=llm,
                    token_limit=token_limit,
                    model_cost=model_cost,
                )
                for src, cmp in pairs:
                    out.append(
                        function(
                            src,
                            cmp,
                            *args,
                            **kwargs,
                            language=language,
                            llm=llm,
                            token_limit=token_limit,
                            model_cost=model_cost,
                        )
                    )
                with open(out_file, "w") as f:
                    json.dump(out, f)

            sig1 = inspect.signature(function)
            sig2 = inspect.signature(func)
            func.__signature__ = sig2.replace(
                parameters=tuple(
                    list(sig2.parameters.values())[:6]
                    + list(sig1.parameters.values())[2:-1]
                )
            )
        else:

            def func(
                target: Annotated[
                    str, typer.Option("--target", "-t", help="Target file to evaluate.")
                ],
                out_file: Annotated[
                    str,
                    typer.Option("--out-file", "-o", help="Output JSON file to write."),
                ],
                language: Annotated[
                    str,
                    typer.Option(
                        "--language",
                        "-l",
                        help="The language of the source code.",
                        click_type=click.Choice(sorted(LANGUAGES)),
                    ),
                ],
                splitting_method: Annotated[
                    str,
                    typer.Option(
                        "--method",
                        "-m",
                        click_type=click.Choice(SPLITTING_METHODS.keys()),
                        help="Method to use for pairing\
                              segments of target and reference files.",
                    ),
                ] = "file",
                llm_name: Annotated[
                    str,
                    typer.Option(
                        "--llm",
                        help="The custom name of the model set with 'janus llm add'.",
                    ),
                ] = "gpt-3.5-turbo",
                *args,
                **kwargs,
            ):
                out = []
                with open(target, "r") as f:
                    target_contents = f.read()

                llm, token_limit, model_cost = load_model(llm_name)
                strings = SPLITTING_METHODS[splitting_method](
                    target_contents,
                    target_file=target,
                    out_file=out_file,
                    lang=language,
                    llm=llm,
                    token_limit=token_limit,
                    model_cost=model_cost,
                )
                for string in strings:
                    out.append(
                        function(
                            string,
                            *args,
                            **kwargs,
                            language=language,
                            llm=llm,
                            token_limit=token_limit,
                            model_cost=model_cost,
                        )
                    )
                with open(out_file, "w") as f:
                    json.dump(out, f)

            sig1 = inspect.signature(function)
            sig2 = inspect.signature(func)
            func.__signature__ = sig2.replace(
                parameters=tuple(
                    list(sig2.parameters.values())[:5]
                    + list(sig1.parameters.values())[1:-1]
                )
            )
        if name is None:
            func.__name__ = function.__name__
        else:
            func.__name__ = name
        if help is None:
            func = evaluate.command()(func)
        else:
            func = evaluate.command(help=help)(func)
        return function

    return decorator
