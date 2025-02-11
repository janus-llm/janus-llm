from pathlib import Path
from typing import List, Optional

import click
import typer
from typing_extensions import Annotated

from janus.cli.constants import get_subclasses
from janus.converter.converter import Converter
from janus.language.naive.registry import CUSTOM_SPLITTERS
from janus.utils.enums import LANGUAGES


def aggregate(
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
            help="The directory to store failure files during translation",
        ),
    ] = None,
    max_prompts: Annotated[
        int,
        typer.Option(
            "--max-prompts",
            "-m",
            help="The maximum number of times to prompt a model on one functional block "
            "before exiting the application. This is to prevent wasting too much money.",
        ),
    ] = 10,
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite/--preserve",
            help="Whether to overwrite existing files in the output directory",
        ),
    ] = False,
    temperature: Annotated[
        float,
        typer.Option("--temperature", "-t", help="Sampling temperature.", min=0, max=2),
    ] = 0.7,
    collection: Annotated[
        str,
        typer.Option(
            "--collection",
            "-c",
            help="If set, will put the translated result into a Chroma DB "
            "collection with the name provided.",
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
    intermediate_converters: Annotated[
        List[str],
        typer.Option(
            "-C",
            "--converter",
            help="Name of an intermediate converter to use",
            click_type=click.Choice([c.__name__ for c in get_subclasses(Converter)]),
        ),
    ] = ["Documenter"],
):
    from janus.cli.constants import db_loc, get_collections_config
    from janus.converter.aggregator import Aggregator

    converter_subclasses = get_subclasses(Converter)
    converter_subclasses_map = {c.__name__: c for c in converter_subclasses}
    model_arguments = dict(temperature=temperature)
    collections_config = get_collections_config()
    converters = []
    for ic in intermediate_converters:
        converters.append(
            converter_subclasses_map[ic](
                model=llm_name,
                model_arguments=model_arguments,
                source_language=language,
                max_prompts=max_prompts,
                db_path=db_loc,
                db_config=collections_config,
                splitter_type=splitter_type,
            )
        )

    aggregator = Aggregator(
        intermediate_converters=converters,
        model=llm_name,
        model_arguments=model_arguments,
        source_language=language,
        max_prompts=max_prompts,
        db_path=db_loc,
        db_config=collections_config,
        splitter_type=splitter_type,
        prompt_templates="basic_aggregation",
    )
    aggregator.translate(input_dir, output_dir, failure_dir, overwrite, collection)
