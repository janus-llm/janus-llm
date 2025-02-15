import json
from pathlib import Path
from typing import Optional

import click
import typer
from typing_extensions import Annotated

from janus.cli.constants import CONVERTERS
from janus.converter.chain import ConverterChain
from janus.converter.pool import ConverterPool
from janus.utils.enums import LANGUAGES


def instiantiate(x):
    if isinstance(x, dict):
        if "type" in x:
            if "args" not in x:
                x["args"] = []
            x["args"] = [instiantiate(a) for a in x["args"]]
            if "kwargs" not in x:
                x["kwargs"] = {}
            x["kwargs"] = {k: instiantiate(x["kwargs"][k]) for k in x["kwargs"]}
            if x["type"] not in CONVERTERS:
                raise ValueError(f"Error: {x['type']} is not a Converter")
            return CONVERTERS[x["type"]](*x["args"], **x["kwargs"])
        else:
            return {k: instiantiate(x[k]) for k in x}
    elif isinstance(x, list):
        return [instiantiate(a) for a in x]
    else:
        return x


def instiantiate_pipeline(
    pipeline: list[dict],
    language: str = "text",
    model: str = "gpt-4o",
    use_janus_inputs: None | bool = None,
):
    if "kwargs" not in pipeline[0]:
        pipeline[0]["kwargs"] = {}
    pipeline[0]["kwargs"].update(source_language=language, model=model)
    if use_janus_inputs is not None:
        pipeline[0]["kwargs"].update(use_janus_inputs=use_janus_inputs)
    converters = [instiantiate(pipeline[0])]
    for p in pipeline[1:]:
        if not isinstance(converters[-1], ConverterPool) and p["type"] != "ConverterPool":
            p["kwargs"].update(
                source_language=converters[-1].target_language, model=model
            )
        converters.append(instiantiate(p))
    return ConverterChain(*converters)


def pipeline(
    pipeline_file: Annotated[
        Path, typer.Option("-p", "--pipeline", help="Name of pipeline file to use")
    ],
    input_dir: Annotated[
        Path,
        typer.Option(
            "--input",
            "-i",
            help="The directory containing the source code to be translated. "
            "The files should all be in one flat directory.",
        ),
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
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output", "-o", help="The directory to store the translated code in."
        ),
    ],
    llm_name: Annotated[
        str,
        typer.Option(
            "--llm",
            "-L",
            help="The custom name of the model set with 'janus llm add'.",
        ),
    ],
    failure_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--failure-directory",
            "-f",
            help="The directory to store failure files during documentation",
        ),
    ] = None,
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite/--preserve",
            help="Whether to overwrite existing files in the output directory",
        ),
    ] = False,
    use_janus_inputs: Annotated[
        Optional[bool],
        typer.Option(
            "-j",
            "--use-janus-inputs",
            help="Present if converter chain should use janus input files",
        ),
    ] = None,
):
    with open(pipeline_file, "r") as f:
        json_obj = json.load(f)
    pipeline = instiantiate_pipeline(
        json_obj, language=language, model=llm_name, use_janus_inputs=use_janus_inputs
    )
    pipeline.translate(
        input_directory=input_dir,
        output_directory=output_dir,
        failure_directory=failure_dir,
        overwrite=overwrite,
    )
