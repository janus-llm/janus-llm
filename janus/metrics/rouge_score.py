import click
import typer
from rouge import Rouge
from typing_extensions import Annotated

from .metric import metric


@metric(help="ROUGE score")
def rouge(
    target: str,
    reference: str,
    n_gram: Annotated[
        int,
        str,
        typer.Option(
            "--n-gram",
            "-n",
            help=(
                "The n-gram overlap calculated for ROUGE-N. Can be an integer or `L`. "
                "For example, ROUGE-2 refers to the overlap of bigrams between the "
                "target and reference. `L` refers to the longest matching sequence."
            ),
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
        n_gram: The n-gram overlap calculated for ROUGE-N. Can be an integer or `L`.

    Returns:
        The ROUGE score.
    """
    import nltk

    nltk.download("punkt", quiet=True)
    if isinstance(n_gram, int):
        metric_name = "rouge-n"
        metric_name_output = f"rouge-{n_gram}"
        max_n = n_gram
    elif str(n_gram).lower() == "l":
        metric_name = "rouge-l"
        metric_name_output = "rouge-l"
        max_n = 4
    else:
        raise ValueError("Invalid n_gram value. Must be an integer or `L`.")

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
