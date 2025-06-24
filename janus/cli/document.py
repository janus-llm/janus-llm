from pathlib import Path
from typing import Any, Optional

import click
import typer
from typing_extensions import Annotated

from janus.cli.constants import REFINERS, key_value_arg
from janus.language.naive.registry import CUSTOM_SPLITTERS
from janus.utils.enums import LANGUAGES


def document(
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
    doc_mode: Annotated[
        str,
        typer.Option(
            "--doc-mode",
            "-d",
            help="The documentation mode.",
            click_type=click.Choice(
                ["cloze", "summary", "multidoc", "pseudocode", "requirements"]
            ),
        ),
    ] = "cloze",
    comments_per_request: Annotated[
        int,
        typer.Option(
            "--comments-per-request",
            "-rc",
            help="The maximum number of comments to generate per request when using "
            "Cloze documentation mode.",
        ),
    ] = None,
    drop_comments: Annotated[
        bool,
        typer.Option(
            "--drop-comments/--keep-comments",
            help="Whether to drop or keep comments in the code sent to the LLM",
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
            help="Present if converter should use janus files as inputs",
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
):
    from janus.cli.constants import db_loc, get_collections_config
    from janus.converter.document import (
        ClozeDocumenter,
        Documenter,
        MultiDocumenter,
        PseudocodeDocumenter,
    )
    from janus.converter.requirements import RequirementsDocumenter

    refiner_types = [REFINERS[r] for r in refiner_types]
    model_arguments: dict[str, Any] = {}
    if model_kwargs:
        kwargs = dict(map(key_value_arg, model_kwargs))
        model_arguments.update(kwargs)

    collections_config = get_collections_config()
    kwargs = dict(
        model=llm_name,
        model_kwargs=model_arguments,
        source_language=language,
        max_prompts=max_prompts,
        max_tokens=max_tokens,
        db_path=db_loc,
        db_config=collections_config,
        splitter_type=splitter_type,
        refiner_types=refiner_types,
        retriever_type=retriever_type,
        use_janus_inputs=use_janus_inputs,
        combine_output=not separate_outputs,
    )
    if doc_mode == "cloze":
        documenter = ClozeDocumenter(comments_per_request=comments_per_request, **kwargs)
    elif doc_mode == "multidoc":
        documenter = MultiDocumenter(drop_comments=drop_comments, **kwargs)
    elif doc_mode == "pseudocode":
        documenter = PseudocodeDocumenter(drop_comments=drop_comments, **kwargs)
    elif doc_mode == "requirements":
        documenter = RequirementsDocumenter(drop_comments=drop_comments, **kwargs)
    else:
        documenter = Documenter(drop_comments=drop_comments, **kwargs)

    documenter.translate(input_path, output_dir, failure_dir, overwrite, collection)
