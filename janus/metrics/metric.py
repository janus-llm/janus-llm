import inspect
import json
from typing import Callable, Optional

import click
import typer
from typing_extensions import Annotated

from janus.cli.constants import CONVERTERS
from janus.converter.converter import Converter
from janus.llm import load_model
from janus.llm.model_callbacks import COST_PER_1K_TOKENS
from janus.metrics.cli import evaluate
from janus.metrics.file_pairing import FILE_PAIRING_METHODS
from janus.metrics.splitting import SPLITTING_METHODS
from janus.utils.enums import LANGUAGES
from janus.utils.logger import create_logger
from janus.utils.progress import track

log = create_logger(__name__)


def metric(
    name: None | str = None,
    help: None | str = None,
    use_reference: bool = True,
) -> Callable:
    """Returns a decorator to add a given metric to the cli

    Metrics must follow the format (src_str, cmp_str, **other_params)

    Arguments:
        name: The name of the metric. If None, the function name is used.
        help: The help text for the metric.
        use_reference: Whether the metric requires a reference string.

    Returns:
        The decorator function.
    """

    def decorator(function):
        if use_reference:

            def func(
                out_file: Annotated[
                    str,
                    typer.Option("--out-file", "-o", help="Output JSON file to write."),
                ],
                language: Annotated[
                    Optional[str],
                    typer.Option(
                        "--language",
                        "-l",
                        help="The language of the source code.",
                        click_type=click.Choice(sorted(LANGUAGES)),
                    ),
                ] = None,
                target: Annotated[
                    Optional[str],
                    typer.Option(
                        "--target",
                        "-t",
                        help="Target file or string to evaluate.",
                    ),
                ] = None,
                reference: Annotated[
                    Optional[str],
                    typer.Option(
                        "--reference",
                        "-r",
                        help="Reference file or string to use as reference/baseline.",
                    ),
                ] = None,
                file_pairing_method: Annotated[
                    str,
                    typer.Option(
                        "--method",
                        "-m",
                        click_type=click.Choice(FILE_PAIRING_METHODS.keys()),
                        help="Method to use for pairing\
                              segments of target and reference files \
                                (ignored for json).",
                    ),
                ] = "file",
                llm_name: Annotated[
                    str,
                    typer.Option(
                        "--llm",
                        "-L",
                        help="The custom name of the model set with 'janus llm add'.",
                    ),
                ] = "gpt-4o",
                progress: Annotated[
                    bool,
                    typer.Option(
                        "--progress",
                        "-p",
                        help="Whether to display a progress bar.",
                        is_flag=True,
                    ),
                ] = False,
                use_janus_inputs: Annotated[
                    bool,
                    typer.Option(
                        "-j",
                        "--use-janus-inputs",
                        help="present if janus output files should be evaluated",
                    ),
                ] = False,
                use_strings: Annotated[
                    bool,
                    typer.Option(
                        "--string",
                        "-S",
                        help="Indicate that the target and reference are strings",
                        is_flag=True,
                    ),
                ] = False,
                *args,
                **kwargs,
            ):
                out = []
                llm = load_model(llm_name)
                if use_janus_inputs:
                    with open(target, "r") as f:
                        target_obj = json.load(f)
                    with open(reference, "r") as f:
                        reference_obj = json.load(f)
                    converter_cls = CONVERTERS.get(
                        target_obj["metadata"].get("converter_name", "Converter"),
                        Converter,
                    )
                    out = converter_cls.eval_obj_reference(
                        target=target_obj,
                        reference=reference_obj,
                        metric_func=function,
                        *args,
                        **kwargs,
                    )
                else:
                    if use_strings:
                        target_contents = target
                        reference_contents = reference
                    else:
                        with open(target, "r") as f:
                            target_contents = f.read()
                        with open(reference, "r") as f:
                            reference_contents = f.read()
                    pairs = FILE_PAIRING_METHODS[file_pairing_method](
                        target_contents,
                        reference_contents,
                        target_file=None if use_strings else target,
                        reference_file=None if use_strings else reference,
                        out_file=out_file,
                        lang=language,
                        llm=llm,
                        token_limit=llm.token_limit,
                        model_cost=COST_PER_1K_TOKENS[llm.model_id],
                    )
                    out = apply_function_pairs(
                        pairs,
                        function,
                        progress,
                        language,
                        llm,
                        llm.token_limit,
                        COST_PER_1K_TOKENS[llm.model_id],
                        *args,
                        **kwargs,
                    )
                with open(out_file, "w") as f:
                    log.info(f"Writing output to {out_file}")
                    json.dump(out, f)

            sig1 = inspect.signature(function)
            sig2 = inspect.signature(func)
            func.__signature__ = sig2.replace(
                parameters=tuple(
                    list(sig2.parameters.values())[:9]
                    + list(sig1.parameters.values())[2:-1]
                )
            )
        else:

            def func(
                out_file: Annotated[
                    str,
                    typer.Option("--out-file", "-o", help="Output JSON file to write."),
                ],
                language: Annotated[
                    Optional[str],
                    typer.Option(
                        "--language",
                        "-l",
                        help="The language of the source code.",
                        click_type=click.Choice(sorted(LANGUAGES)),
                    ),
                ] = None,
                target: Annotated[
                    Optional[str],
                    typer.Option(
                        "--target", "-t", help="Target file or string to evaluate."
                    ),
                ] = None,
                use_janus_inputs: Annotated[
                    bool,
                    typer.Option(
                        "-j",
                        "--use-janus-inputs",
                        help="whether to use a janus output file as input",
                    ),
                ] = False,
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
                        "-L",
                        help="The custom name of the model set with 'janus llm add'.",
                    ),
                ] = "gpt-4o",
                progress: Annotated[
                    bool,
                    typer.Option(
                        "--progress",
                        "-p",
                        help="Whether to display a progress bar.",
                        is_flag=True,
                    ),
                ] = False,
                use_strings: Annotated[
                    bool,
                    typer.Option(
                        "--string",
                        "-S",
                        help="Indicate that the target and reference are strings",
                        is_flag=True,
                    ),
                ] = False,
                *args,
                **kwargs,
            ):
                llm = load_model(llm_name)
                if use_janus_inputs:
                    with open(target, "r") as f:
                        target_obj = json.load(f)
                    converter_cls = CONVERTERS.get(
                        target_obj["metadata"].get("converter_name", "Converter"),
                        Converter,
                    )
                    out = converter_cls.eval_obj(
                        target=target_obj, metric_func=function, *args, **kwargs
                    )
                else:
                    if use_strings:
                        target_contents = target
                    else:
                        with open(target, "r") as f:
                            target_contents = f.read()

                    strings = SPLITTING_METHODS[splitting_method](
                        target_contents,
                        target_file=target if not use_strings else None,
                        out_file=out_file,
                        lang=language,
                        llm=llm,
                        token_limit=llm.token_limit,
                        model_cost=COST_PER_1K_TOKENS[llm.model_id],
                    )
                    out = apply_function_strings(
                        strings,
                        function,
                        progress,
                        language,
                        llm,
                        llm.token_limit,
                        COST_PER_1K_TOKENS[llm.model_id],
                        *args,
                        **kwargs,
                    )
                with open(out_file, "w") as f:
                    log.info(f"Writing output to {out_file}")
                    json.dump(out, f)

            sig1 = inspect.signature(function)
            sig2 = inspect.signature(func)
            func.__signature__ = sig2.replace(
                parameters=tuple(
                    list(sig2.parameters.values())[:7]
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


def apply_function_pairs(
    pairs,
    function,
    progress,
    language,
    llm,
    token_limit,
    model_cost,
    *args,
    **kwargs,
):
    out = []
    pair_keys = None
    if isinstance(pairs, dict):
        pair_keys = list(pairs.keys())
        pair_values = list(pairs.values())
    else:
        pair_values = pairs
    if progress:
        loop = track(pair_values, description="Evaluating pairs")
    else:
        loop = pair_values
    for src, cmp in loop:
        if not (isinstance(src, str) and isinstance(cmp, str)):
            out.append(False)
        else:
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
    if pair_keys is not None:
        return {k: v for k, v in zip(pair_keys, out)}
    return out


def apply_function_strings(
    strings, function, progress, language, llm, token_limit, model_cost, *args, **kwargs
):
    out = []
    string_keys = None
    if isinstance(strings, dict):
        string_keys = list(strings.keys())
        string_values = list(strings.values())
    else:
        string_values = strings
    if progress:
        loop = track(string_values, description="Evaluating strings")
    else:
        loop = string_values
    for string in loop:
        if not isinstance(string, str):
            out.append(False)
        else:
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
    if string_keys is not None:
        return {k: v for k, v in zip(string_keys, out)}
    return out
