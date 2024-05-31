import inspect
import json
from pathlib import Path
from typing import Callable, Optional

import click
import typer
from typing_extensions import Annotated

from janus.llm import load_model
from janus.utils.enums import LANGUAGES
from janus.utils.logger import create_logger

from ..utils.progress import track
from .cli import evaluate
from .file_pairing import FILE_PAIRING_METHODS
from .splitting import SPLITTING_METHODS

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
                        help="Target file to evaluate.",
                    ),
                ] = None,
                reference: Annotated[
                    Optional[str],
                    typer.Option(
                        "--reference",
                        "-r",
                        help="Reference file to use as reference/baseline.",
                    ),
                ] = None,
                json_file_name: Annotated[
                    Optional[str],
                    typer.Option(
                        "--json",
                        "-j",
                        help="Json file to extract pairs from \
                            (if set ignores --target and --reference)",
                    ),
                ] = None,
                target_key: Annotated[
                    str,
                    typer.Option(
                        "--target-key",
                        "-tk",
                        help="json key to extract list of target strings",
                    ),
                ] = "target",
                reference_key: Annotated[
                    str,
                    typer.Option(
                        "--reference-key",
                        "-rk",
                        help="json key to extract list of reference strings",
                    ),
                ] = "reference",
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
                ] = "gpt-3.5-turbo",
                progress: Annotated[
                    bool,
                    typer.Option(
                        "--progress",
                        "-p",
                        help="Whether to display a progress bar.",
                        is_flag=True,
                    ),
                ] = False,
                *args,
                **kwargs,
            ):
                out = []
                llm, token_limit, model_cost = load_model(llm_name)
                if json_file_name is not None:
                    with open(json_file_name, "r") as f:
                        json_obj = json.load(f)
                    pairs = {}
                    for key in json_obj:
                        doc = json_obj[key]
                        ref = doc[reference_key]
                        for model_key in doc:
                            model_dict = doc[model_key]
                            if not isinstance(model_dict, dict):
                                continue
                            if target_key not in model_dict:
                                continue
                            if model_key not in pairs:
                                pairs[model_key] = []
                            for k in model_dict[target_key]:
                                pairs[model_key] += list(
                                    zip(
                                        model_dict[target_key][k],
                                        ref[k],
                                    )
                                )
                elif target is not None and reference is not None:
                    with open(target, "r") as f:
                        target_contents = f.read()

                    with open(reference, "r") as f:
                        reference_contents = f.read()
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
                else:
                    raise ValueError(
                        "Error, must specify either json or target and reference files"
                    )
                if isinstance(pairs, dict):
                    out = {}
                    for k in pairs:
                        out[k] = apply_function_pairs(
                            pairs[k],
                            function,
                            progress,
                            language,
                            llm,
                            token_limit,
                            model_cost,
                            *args,
                            **kwargs,
                        )
                else:
                    out = apply_function_pairs(
                        pairs,
                        function,
                        progress,
                        language,
                        llm,
                        token_limit,
                        model_cost,
                        *args,
                        **kwargs,
                    )
                out_file = Path(out_file)
                out_file.parent.mkdir(parents=True, exist_ok=True)
                with open(out_file, "w") as f:
                    json.dump(out, f)
                    log.info(f"Saved results to file: {out_file}")

            sig1 = inspect.signature(function)
            sig2 = inspect.signature(func)
            func.__signature__ = sig2.replace(
                parameters=tuple(
                    list(sig2.parameters.values())[:10]
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
                    typer.Option("--target", "-t", help="Target file to evaluate."),
                ] = None,
                json_file_name: Annotated[
                    Optional[str],
                    typer.Option(
                        "--json",
                        "-j",
                        help="Json file to extract pairs from \
                            (if set ignores --target)",
                    ),
                ] = None,
                target_key: Annotated[
                    str,
                    typer.Option(
                        "--target-key",
                        "-tk",
                        help="json key to extract list of target strings",
                    ),
                ] = "target",
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
                ] = "gpt-3.5-turbo",
                progress: Annotated[
                    bool,
                    typer.Option(
                        "--progress",
                        "-p",
                        help="Whether to display a progress bar.",
                        is_flag=True,
                    ),
                ] = False,
                *args,
                **kwargs,
            ):
                out = []
                llm, token_limit, model_cost = load_model(llm_name)
                if json_file_name is not None:
                    with open(json_file_name, "r") as f:
                        json_obj = json.load(f)
                    strings = {}
                    for key in json_obj:
                        doc = json_obj[key]
                        for model_name in doc:
                            model_dict = doc[model_name]
                            if not isinstance(model_dict, dict):
                                continue
                            if target_key not in model_dict:
                                continue
                            if model_name not in strings:
                                strings[model_name] = []
                            for k in model_dict:
                                strings[model_name].append(model_dict[k])
                        # strings += list(json_obj[key][target_key].values())
                elif target is not None:
                    with open(target, "r") as f:
                        target_contents = f.read()

                    strings = SPLITTING_METHODS[splitting_method](
                        target_contents,
                        target_file=target,
                        out_file=out_file,
                        lang=language,
                        llm=llm,
                        token_limit=token_limit,
                        model_cost=model_cost,
                    )
                else:
                    raise ValueError(
                        "Error: must specify either json file or target file"
                    )
                if isinstance(strings, dict):
                    out = {}
                    for k in strings:
                        out[k] = apply_function_strings(
                            strings[k],
                            function,
                            progress,
                            language,
                            llm,
                            token_limit,
                            model_cost,
                            *args,
                            **kwargs,
                        )
                else:
                    out = apply_function_strings(
                        strings,
                        function,
                        progress,
                        language,
                        llm,
                        token_limit,
                        model_cost,
                        *args,
                        **kwargs,
                    )
                out_file = Path(out_file)
                out_file.parent.mkdir(parents=True, exist_ok=True)
                with open(out_file, "w") as f:
                    json.dump(out, f)
                    log.info(f"Saved results to file: {out_file}")

            sig1 = inspect.signature(function)
            sig2 = inspect.signature(func)
            func.__signature__ = sig2.replace(
                parameters=tuple(
                    list(sig2.parameters.values())[:8]
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
    if progress:
        loop = track(pairs, description="Evaluating pairs")
    else:
        loop = pairs
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
    return out


def apply_function_strings(
    strings, function, progress, language, llm, token_limit, model_cost, *args, **kwargs
):
    out = []
    if progress:
        loop = track(strings, description="Evaluating strings")
    else:
        loop = strings
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
    return out
