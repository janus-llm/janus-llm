from pathlib import Path
from typing import Optional

import click
import typer
from typing_extensions import Annotated

from janus.cli.constants import REFINERS
from janus.language.naive.registry import CUSTOM_SPLITTERS
from janus.utils.enums import LANGUAGES


def llm_self_eval(
    input_dir: Annotated[
        Path,
        typer.Option(
            "--input",
            "-i",
            help="The directory containing the source code to be evaluated. "
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
        typer.Option("--output", "-o", help="The directory to store the evaluations in."),
    ],
    failure_dir: Annotated[
        Optional[Path],
        typer.Option(
            "--failure-directory",
            "-f",
            help="The directory to store failure files during translation",
        ),
    ] = None,
    llm_name: Annotated[
        str,
        typer.Option(
            "--llm",
            "-L",
            help="The custom name of the model set with 'janus llm add'.",
        ),
    ] = "gpt-4o",
    evaluation_type: Annotated[
        str,
        typer.Option(
            "--evaluation-type",
            "-e",
            help="Type of output to evaluate.",
            click_type=click.Choice(["incose", "comments"]),
        ),
    ] = "incose",
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
    refiner_types: Annotated[
        list[str],
        typer.Option(
            "-r",
            "--refiner",
            help="List of refiner types to use. Add -r for each refiner to use in\
                refinement chain",
            click_type=click.Choice(list(REFINERS.keys())),
        ),
    ] = ["JanusRefiner"],
    eval_items_per_request: Annotated[
        int,
        typer.Option(
            "--eval-items-per-request",
            "-rc",
            help="The maximum number of evaluation items per request",
        ),
    ] = None,
    max_tokens: Annotated[
        int,
        typer.Option(
            "--max-tokens",
            "-M",
            help="The maximum number of tokens the model will take in. "
            "If unspecificed, model's default max will be used.",
        ),
    ] = None,
    use_janus_inputs: Annotated[
        bool,
        typer.Option(
            "-j",
            "--use-janus-inputs",
            help="Prsent if translator should use janus files as inputs",
        ),
    ] = False,
):
    from janus.converter.evaluate import InlineCommentEvaluator, RequirementEvaluator

    model_arguments = dict(temperature=temperature)
    refiner_types = [REFINERS[r] for r in refiner_types]
    kwargs = dict(
        eval_items_per_request=eval_items_per_request,
        model=llm_name,
        model_arguments=model_arguments,
        source_language=language,
        max_prompts=max_prompts,
        max_tokens=max_tokens,
        splitter_type=splitter_type,
        refiner_types=refiner_types,
        use_janus_inputs=use_janus_inputs,
    )
    # Setting parser type here
    if evaluation_type == "incose":
        evaluator = RequirementEvaluator(**kwargs)
    elif evaluation_type == "comments":
        evaluator = InlineCommentEvaluator(**kwargs)

    evaluator.translate(input_dir, output_dir, failure_dir, overwrite, collection)
