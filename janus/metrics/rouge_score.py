import click
import typer
from rouge_score import rouge_scorer
from typing_extensions import Annotated

from janus.metrics.metric import metric


@metric(help="ROUGE score")
def rouge(
    target: str,
    reference: str,
    granularity: Annotated[
        str,
        typer.Option(
            "--granularity",
            "-g",
            help=(
                "The granularity of the ROUGE score. `n` refers to "
                "ROUGE-N, `l` refers to ROUGE-L."
            ),
            click_type=click.Choice(["n", "l"]),
        ),
    ] = "n",
    n_gram: Annotated[
        int,
        typer.Option(
            "--n-gram",
            "-n",
            help=("The n-gram overlap calculated for ROUGE-N. Can be an integer."),
        ),
    ] = 2,
    score_type: Annotated[
        str,
        typer.Option(
            "--score",
            "-s",
            help=(
                "Whether to use the F-score, precision, or recall. For example, `f` "
                "refers to the F-score, `p` refers to precision, and `r` refers to "
                "recall."
            ),
            click_type=click.Choice(["f", "p", "r"]),
        ),
    ] = "f",
    **kwargs,
) -> float:
    """Calculate the ROUGE Score.

    Arguments:
        target: The target text.
        reference: The reference text.
        granularity: The granularity of the ROUGE score. `n` refers to ROUGE-N, `l`
            refers to ROUGE-L.
        n_gram: The n-gram overlap calculated for ROUGE-N. Can be an integer.
        score_type: Whether to use the F-score, precision, or recall. For example, `f`
            refers to the F-score, `p` refers to precision, and `r` refers to recall.

    Returns:
        The ROUGE score.
    """
    if granularity.lower() == "n":
        metric_name = f"rouge{n_gram}"
    elif granularity.lower() == "l":
        metric_name = "rougeL"
    else:
        raise ValueError("Invalid granularity. Must be one of `n` or `l`")

    evaluator = rouge_scorer.RougeScorer(
        [metric_name],
        use_stemmer=True,
    )
    scores = evaluator.score(target, reference)
    scores_fpr = scores[metric_name]
    if score_type.lower() == "f":
        score = scores_fpr.fmeasure
    elif score_type.lower() == "p":
        score = scores_fpr.precision
    elif score_type.lower() == "r":
        score = scores_fpr.recall
    else:
        raise ValueError("Invalid score type. Must be one of `f`, `p`, or `r`.")
    return score
