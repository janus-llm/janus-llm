from typing import Optional

import click
import typer
from sacrebleu import sentence_bleu

from .metric import metric

# from sacrebleu import sentence_chrf


@metric()
def bleu(
    target: str,
    reference: str,
    smooth_method: str = typer.Option(
        default="exp", click_type=click.Choice(["exp", "floor", "add-k", "none"])
    ),
    smooth_value: Optional[float] = typer.Option(
        default=None,
    ),
    lowercase: bool = typer.Option(
        default=False,
    ),
    use_effective_order: bool = typer.Option(
        default=True,
    ),
):
    score = sentence_bleu(
        target,
        [reference],
        smooth_method=smooth_method,
        smooth_value=smooth_value,
        lowercase=lowercase,
        use_effective_order=use_effective_order,
    )
    return float(score.score)
