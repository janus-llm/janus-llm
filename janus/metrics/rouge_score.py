import click
import nltk
import typer
from rouge import Rouge
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
                "ROUGE-N, `l` refers to ROUGE-L, and `w` refers to ROUGE-W."
            ),
            click_type=click.Choice(["n", "l", "w"]),
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
            refers to ROUGE-L, and `w` refers to ROUGE-W.
        n_gram: The n-gram overlap calculated for ROUGE-N. Can be an integer.
        score_type: Whether to use the F-score, precision, or recall. For example, `f`
            refers to the F-score, `p` refers to precision, and `r` refers to recall.

    Returns:
        The ROUGE score.
    """
    nltk.download("punkt", quiet=True)

    if granularity.lower() == "n":
        metric_name = "rouge-n"
        metric_name_output = f"rouge-{n_gram}"
        max_n = n_gram
    elif granularity.lower() == "l":
        metric_name = "rouge-l"
        metric_name_output = "rouge-l"
        max_n = 4
    elif granularity.lower() == "w":
        metric_name = "rouge-w"
        metric_name_output = "rouge-w"
        max_n = 4
    else:
        raise ValueError("Invalid granularity. Must be one of `n`, `l`, or `w`.")

    if score_type.lower() not in ["f", "p", "r"]:
        raise ValueError("Invalid score type. Must be one of `f`, `p`, or `r`.")

    evaluator = Rouge(
        metrics=[metric_name],
        max_n=max_n,
        limit_length=False,
        length_limit=1_000,
        length_limit_type="words",
        apply_avg=False,
        apply_best=False,
        alpha=0.5,  # Default F1_score
        weight_factor=1.2,
        stemming=True,
    )
    scores = evaluator.get_scores(target, reference)
    return scores[metric_name_output][0][score_type.lower()][0]
