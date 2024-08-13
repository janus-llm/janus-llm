from typing import Annotated, Optional

import click
import typer
from sacrebleu import sentence_bleu

from janus.metrics.metric import metric

# from sacrebleu import sentence_chrf


@metric(help="BLEU score using sacrebleu")
def bleu(
    target: str,
    reference: str,
    smooth_method: Annotated[
        str,
        typer.Option(
            click_type=click.Choice(["exp", "floor", "add-k", "none"]),
            help="Smoothing method to use.",
        ),
    ] = "exp",
    smooth_value: Annotated[
        Optional[float],
        typer.Option(
            help="Smoothing value (only for 'floor' and 'add-k').",
        ),
    ] = None,
    lowercase: Annotated[
        bool,
        typer.Option(
            help="Whether to lowercase the data.",
        ),
    ] = False,
    use_effective_order: Annotated[
        bool,
        typer.Option(
            help="Whether to use n-gram orders without matches.",
        ),
    ] = True,
    **kwargs,
) -> float:
    """Computes BLEU score using sacrebleu

    Arguments:
        target: The target text.
        reference: The reference text.
        smooth_method: smoothing method to use.
        smooth_value: smoothing value (only for floor and add-k).
        lowercase: whether to lowercase the data.
        use_effective_order: Don't use n-gram orders without matches.

    Returns:
        The BLEU score float.
    """
    score = sentence_bleu(
        target,
        [reference],
        smooth_method=smooth_method,
        smooth_value=smooth_value,
        lowercase=lowercase,
        use_effective_order=use_effective_order,
    )
    # Dividing by 100 to get the score in the range [0, 1]
    # sacrebleu gives the score in percentage
    return float(score.score) / 100.0
