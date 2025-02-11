from pathlib import Path
from typing import Optional

import click
import typer
from typing_extensions import Annotated

from janus.cli.constants import REFINERS
from janus.language.naive.registry import CUSTOM_SPLITTERS
from janus.utils.enums import LANGUAGES


def diagram(
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
    diagram_type: Annotated[
        str,
        typer.Option(
            "--diagram-type", "-dg", help="Diagram type to generate in PLANTUML"
        ),
    ] = "Activity",
    add_documentation: Annotated[
        bool,
        typer.Option(
            "--add-documentation/--no-documentation",
            "-ad",
            help="Whether to use documentation in generation",
        ),
    ] = False,
    splitter_type: Annotated[
        str,
        typer.Option(
            "-S",
            "--splitter",
            help="Name of custom splitter to use",
            click_type=click.Choice(list(CUSTOM_SPLITTERS.keys())),
        ),
    ] = "file",
    refiner_types: Annotated[
        list[str],
        typer.Option(
            "-r",
            "--refiner",
            help="List of refiner types to use. Add -r for each refiner to use in\
                refinement chain",
            click_type=click.Choice(list(REFINERS.keys())),
        ),
    ] = ["CodeFormatRefiner"],
    retriever_type: Annotated[
        str,
        typer.Option(
            "-R",
            "--retriever",
            help="Name of custom retriever to use",
            click_type=click.Choice(["active_usings", "language_docs"]),
        ),
    ] = None,
    extract_variables: Annotated[
        bool,
        typer.Option(
            "-ev",
            "--extract-variables",
            help="Present when diagram generator should \
                extract variables before producing diagram",
        ),
    ] = False,
    use_janus_inputs: Annotated[
        bool,
        typer.Option(
            "-j",
            "--use-janus-inputs",
            help="Present when diagram generator should be\
                  be using janus files as inputs",
        ),
    ] = False,
):
    from janus.cli.constants import db_loc, get_collections_config
    from janus.converter.diagram import DiagramGenerator

    refiner_types = [REFINERS[r] for r in refiner_types]
    model_arguments = dict(temperature=temperature)
    collections_config = get_collections_config()
    diagram_generator = DiagramGenerator(
        model=llm_name,
        model_arguments=model_arguments,
        source_language=language,
        max_prompts=max_prompts,
        db_path=db_loc,
        db_config=collections_config,
        splitter_type=splitter_type,
        refiner_types=refiner_types,
        retriever_type=retriever_type,
        diagram_type=diagram_type,
        add_documentation=add_documentation,
        extract_variables=extract_variables,
        use_janus_inputs=use_janus_inputs,
    )
    diagram_generator.translate(input_dir, output_dir, failure_dir, overwrite, collection)


def render(
    input_dir: Annotated[
        str,
        typer.Option(
            "--input",
            "-i",
        ),
    ],
    output_dir: Annotated[str, typer.Option("--output", "-o")],
):
    import json
    import subprocess  # nosec

    from janus.cli.constants import homedir

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    for input_file in input_dir.rglob("*.json"):
        with open(input_file, "r") as f:
            data = json.load(f)

        output_file = output_dir / input_file.relative_to(input_dir).with_suffix(".txt")
        if not output_file.parent.exists():
            output_file.parent.mkdir()

        def _render(obj, ind=0):
            for o in obj["outputs"]:
                if isinstance(o, dict):
                    ind += _render(o, ind)
                else:
                    outfile_new = output_file.with_stem(f"{output_file.stem}_{ind}")
                    text = o.replace("\\n", "\n").strip()
                    outfile_new.write_text(text)
                    jar_path = homedir / ".janus/lib/plantuml.jar"
                    subprocess.run(["java", "-jar", jar_path, outfile_new])  # nosec
                    outfile_new.unlink()
                    ind += 1
            return ind

        _render(data)
