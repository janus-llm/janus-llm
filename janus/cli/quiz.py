from pathlib import Path
from typing import Any, Optional

import click
import typer
from typing_extensions import Annotated

from janus.cli.constants import REFINERS, key_value_arg
from janus.language.naive.registry import CUSTOM_SPLITTERS
from janus.utils.enums import LANGUAGES
from janus.utils.logger import create_logger

log = create_logger(__name__)


def quiz(
    input_dir: Annotated[
        Path,
        typer.Option(
            "--input",
            "-i",
            help="The directory containing the source code the quiz will be based on. "
            "The files should all be in one flat directory.",
        ),
    ],
    source_lang: Annotated[
        str,
        typer.Option(
            "--source-language",
            "-s",
            help="The language of the source code.",
            click_type=click.Choice(sorted(LANGUAGES)),
        ),
    ],
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output", "-o", help="The directory to store the generated quiz in."
        ),
    ],
    target_lang: Annotated[ #TODO REMOVE
        str,
        typer.Option(
            "--target-language",
            "-t",
            help="The desired output language to translate the source code to. The "
            "format can follow a 'language-version' syntax.  Use 'text' to get plaintext"
            "results as returned by the LLM. Examples: `python-3.10`, `mumps`, `java-10`,"
            "text.",
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
    temp: Annotated[
        float,
        typer.Option("--temperature", "-T", help="Sampling temperature.", min=0, max=2),
    ] = 0.7,
    prompt_template: Annotated[
        str,
        typer.Option(
            "--prompt-template",
            "-p",
            help="Name of the Janus prompt template directory or "
            "path to a directory containing those template files.",
        ),
    ] = "quiz/quiz_generator",
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
    retriever_type: Annotated[
        str,
        typer.Option(
            "-R",
            "--retriever",
            help="Name of custom retriever to use",
            click_type=click.Choice(["active_usings", "language_docs"]),
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
            help="Present if translator should use janus files as inputs",
        ),
    ] = False,
    separate_outputs: Annotated[
        bool,
        typer.Option(
            "--separate-outputs",
            help="Present if converter should combine outputs",
        ),
    ] = False,
    model_kwargs: Annotated[
        list[str],
        typer.Option(
            "--kw",
            help=(
                "Keyword arguments to pass to model kwargs. Expects key=val pair."
                " For multiple, supply this argument multiple times. For example,"
                " `--kw max_tokens=4000 --kw temperature=0.7` (this would set the"
                " maximum *output* tokens to 4000, not to be confused with the"
                " --max-tokens/-M argument)"
            ),
        ),
    ] = [],
    quiz_topic: Annotated[
        str,
        typer.Option(
            "--topic",
            help="The topic the quiz should focus on, for example 'algorithms'."
            "If unspecified, the quiz will be general in nature.",
        ),
    ] = None,
    quiz_topic_description: Annotated[
        str,
        typer.Option(
            "--topic-description",
            "-D",
            help="Description of what the quiz topic includes, for example 'Logic and flow of algorithms used in the code'.",
        ),
    ] = None,
):
    from janus.cli.constants import db_loc, get_collections_config
    from janus.converter.quiz_generator import QuizGenerator

    refiner_types = [REFINERS[r] for r in refiner_types]
    try:
        target_language, target_version = target_lang.split("-")
    except ValueError:
        target_language = target_lang
        target_version = None
    # make sure not overwriting input
    if source_lang.lower() == target_language.lower() and input_dir == output_dir:
        log.error("Output files would overwrite input! Aborting...")
        raise ValueError

    model_arguments: dict[str, Any] = {}
    if model_kwargs:
        kwargs = dict(map(key_value_arg, model_kwargs))
        model_arguments.update(kwargs)

    collections_config = get_collections_config()
    quiz_gen = QuizGenerator(
        model=llm_name,
        model_kwargs=model_arguments,
        source_language=source_lang,
        target_language=target_language,
        target_version=target_version,
        max_prompts=max_prompts,
        max_tokens=max_tokens,
        prompt_templates=prompt_template,
        db_path=db_loc,
        db_config=collections_config,
        splitter_type=splitter_type,
        refiner_types=refiner_types,
        retriever_type=retriever_type,
        use_janus_inputs=use_janus_inputs,
        combine_output=not separate_outputs,
        quiz_topic=quiz_topic,
        quiz_topic_description=quiz_topic_description,
    )
    quiz_gen.translate(input_dir, output_dir, failure_dir, overwrite)
