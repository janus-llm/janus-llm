from pathlib import Path
from typing import Any

import click
import typer
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import BaseOutputParser, JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing_extensions import Annotated

from janus.metrics.metric import metric


class LLMMetricOutput(BaseModel):
    """The output of an LLM evaluation metric."""

    thought: str = Field(
        ...,
        description=(
            "The thought process that you took to reach your value determination."
        ),
    )
    value: str | float | int = Field(
        ..., description="The value of the metric described in the prompt."
    )


def load_prompt(path: Path, language: str, parser: BaseOutputParser) -> PromptTemplate:
    """Load a default prompt from a file.

    Arguments:
        path: The path to the file.
        language: The language of the prompt.
        pydantic_model: The Pydantic model to use for parsing the output.

    Returns:
        The prompt text.
    """
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    prompt = PromptTemplate.from_template(
        path.read_text(),
        template_format="f-string",
        partial_variables={
            "language": language,
            "format_instructions": parser.get_format_instructions(),
        },
    )
    return prompt


def evaluate(
    target: str,
    language: str,
    model: str,
    prompt_path: Path,
    reference: str | None = None,
):
    """Calculate the LLM self evaluation score.

    Arguments:
        target: The target text.
        language: The language that the target code is written in.
        prompt_path: The filepath of the prompt text
        reference: The reference text.

    Returns:
        The LLM Evaluation score.
    """
    parser = JsonOutputParser(pydantic_object=LLMMetricOutput)
    prompt = load_prompt(prompt_path, language, parser)
    chain = prompt | model | parser
    try:
        output = (
            chain.invoke(dict(target=target, reference=reference))
            if reference
            else chain.invoke(dict(target=target))
        )
        return output["value"]
    except OutputParserException:
        return False


@metric(use_reference=False, name="llm", help="LLM self-evaluation on a target file")
def llm_evaluate_option(
    target: str,
    metric: Annotated[
        str,
        typer.Option(
            "--metric",
            "-m",
            help=("The pre-defined metric to use for evaluation."),
            click_type=click.Choice(
                [
                    "quality",
                    "clarity",
                    "faithfulness",
                    "completeness",
                    "hallucination",
                    "readability",
                    "usefulness",
                ]
            ),
        ),
    ] = "quality",
    prompt: Annotated[
        str,
        None,
        typer.Option(
            "--prompt",
            "-P",
            help=("A custom prompt in a .txt file to use for evaluation."),
        ),
    ] = None,
    num_eval: Annotated[
        int,
        typer.Option(
            "-n",
            "--num-eval",
            help="Number of times to run the evaluation",
        ),
    ] = 1,
    **kwargs,
) -> Any:
    """CLI option to calculate the LLM self evaluation score.

    Arguments:
        target: The target text.
        reference: The reference text.
        metric: The pre-defined metric to use for evaluation.
        prompt: The prompt text.

    Returns:
        The LLM Evaluation score.
    """
    prompt_path: Path = (
        Path(prompt) if prompt else Path(__file__).parent / "prompts" / f"{metric}.txt"
    )
    if num_eval == 1:
        return evaluate(target, kwargs["language"], kwargs["llm"], prompt_path)
    else:
        return [
            evaluate(target, kwargs["language"], kwargs["llm"], prompt_path)
            for _ in range(num_eval)
        ]


@metric(name="llm-ref", help="LLM self-evaluation on a target file and a reference file")
def llm_evaluate_ref_option(
    target: str,
    reference: str,
    metric: Annotated[
        str,
        typer.Option(
            "--metric",
            "-m",
            help=("The pre-defined metric to use for evaluation."),
            click_type=click.Choice(["faithfulness"]),
        ),
    ] = "faithfulness",
    prompt: Annotated[
        str,
        None,
        typer.Option(
            "--prompt",
            "-P",
            help=("A custom prompt in a .txt file to use for evaluation."),
        ),
    ] = None,
    num_eval: Annotated[
        int,
        typer.Option(
            "-n",
            "--num-eval",
            help="Number of times to run evaluation for pair",
        ),
    ] = 1,
    **kwargs,
) -> Any:
    """CLI option to calculate the LLM self evaluation score, for evaluations which
    require a reference file (e.g. faithfulness)

    Arguments:
        target: The target text.
        reference: The reference text.
        metric: The pre-defined metric to use for evaluation.
        prompt: The prompt text.

    Returns:
        The LLM Evaluation score.
    """
    prompt_path: Path = (
        Path(prompt) if prompt else Path(__file__).parent / "prompts" / f"{metric}.txt"
    )
    if num_eval == 1:
        return evaluate(target, kwargs["language"], kwargs["llm"], prompt_path, reference)
    else:
        return [
            evaluate(target, kwargs["language"], kwargs["llm"], prompt_path, reference)
            for _ in range(num_eval)
        ]
