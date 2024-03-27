from typing import Optional

import click
import typer
from sacrebleu import sentence_bleu

from .metric import metric

# from sacrebleu import sentence_chrf


@metric(help="Compute the bleu score using sacrebleu")
def bleu(
    target: str,
    reference: str,
    smooth_method: str = typer.Option(
        default="exp",
        click_type=click.Choice(["exp", "floor", "add-k", "none"]),
        help="smoothing method to use.",
    ),
    smooth_value: Optional[float] = typer.Option(
        default=None,
        help="smoothing value (only for floor and add-k).",
    ),
    lowercase: bool = typer.Option(
        default=False,
        help="whether to lowercase the data.",
    ),
    use_effective_order: bool = typer.Option(
        default=True,
        help="Don't use n-gram orders without matches.",
    ),
):
    """
    Computes bleu score using sacrebleu
    Arguments:
        target: The target text.
        reference: The reference text.
        smooth_method: smoothing method to use.
        smooth_value: smoothing value (only for floor and add-k).
        lowercase: whether to lowercase the data.
        use_effective_order: Don't use n-gram orders without matches.
    """
    score = sentence_bleu(
        target,
        [reference],
        smooth_method=smooth_method,
        smooth_value=smooth_value,
        lowercase=lowercase,
        use_effective_order=use_effective_order,
    )
    return float(score.score)
