import json
from pathlib import Path
from typing import Any, NotRequired, Optional, TypedDict

import click
import typer
from typing_extensions import Annotated

from janus.cli.constants import CONVERTERS
from janus.converter.converter import Converter
from janus.language.naive.registry import CUSTOM_SPLITTERS
from janus.utils.enums import LANGUAGES


class ConverterDefinition(TypedDict):
    type: str
    converters: NotRequired[list["ConverterDefinition"]]
    kwargs: NotRequired[dict[str, Any]]


PipelineObject = Converter | list["PipelineObject"] | dict[str, "PipelineObject"]


def instantiate(
    pipeline_definition: ConverterDefinition,
    model: str,
    source_language: str | None = None,
    use_janus_inputs: bool | None = None,
) -> Converter:
    """Recursively instantiate converters in a pipeline. If source_language is
    provided, the corresponding argument will be overwritten in the keyword
    arguments for the input converter; same for use_janus_inputs.
    The model will always be overridden.
    """
    # Check converter type for existence, retrieve type constructor
    converter_type = pipeline_definition["type"]
    if converter_type not in CONVERTERS:
        raise ValueError(f"Error: {converter_type} is not a Converter")
    ConverterClass = CONVERTERS[converter_type]

    kwargs = pipeline_definition.get("kwargs", {})
    if "model" not in kwargs:
        kwargs.update(model=model)
    if source_language is not None and "source_language" not in kwargs:
        kwargs.update(source_language=source_language)
    if use_janus_inputs is not None and "use_janus_inputs" not in kwargs:
        kwargs.update(use_janus_inputs=use_janus_inputs)

    if converter_type == "ConverterChain":
        if "converters" not in pipeline_definition:
            raise ValueError(f"Error: {converter_type} requires a 'converter' entry")

        # For converter chains, recursively instantiate components
        converters = []
        for conv_def in pipeline_definition["converters"]:
            converters.append(
                instantiate(
                    pipeline_definition=conv_def,
                    model=model,
                    source_language=source_language,
                    use_janus_inputs=use_janus_inputs,
                )
            )

        kwargs["converters"] = converters

    return ConverterClass(**kwargs)


def instantiate_pipeline(
    pipeline: list[ConverterDefinition],
    language: str = "text",
    model: str = "gpt-4o",
    use_janus_inputs: None | bool = None,
    splitter_type: str = "file",
) -> Converter:
    conv_def = ConverterDefinition(
        type="ConverterChain",
        converters=pipeline,
        kwargs=dict(splitter_type=splitter_type),
    )
    return instantiate(
        conv_def,
        source_language=language,
        model=model,
        use_janus_inputs=use_janus_inputs,
    )


def pipeline(
    pipeline_file: Annotated[
        Path, typer.Option("-p", "--pipeline", help="Name of pipeline file to use")
    ],
    input_path: Annotated[
        Path,
        typer.Option(
            "--input",
            "-i",
            help="The directory containing the source code to be translated"
            "or the path to a file that should be translated."
            "If it's a directory then the files should all be in one flat directory.",
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
    splitter_type: Annotated[
        str,
        typer.Option(
            "-S",
            "--splitter",
            help="Name of custom splitter to use",
            click_type=click.Choice(list(CUSTOM_SPLITTERS.keys())),
        ),
    ] = "file",
):
    with open(pipeline_file, "r") as f:
        json_obj = json.load(f)
    pipeline = instantiate_pipeline(
        json_obj,
        language=language,
        model=llm_name,
        use_janus_inputs=use_janus_inputs,
        splitter_type=splitter_type,
    )
    pipeline.translate(
        input_directory=input_path,
        output_directory=output_dir,
        failure_directory=failure_dir,
        overwrite=overwrite,
    )
