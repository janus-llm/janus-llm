import typer
from sacrebleu import sentence_chrf

from janus.metrics.metric import metric


@metric(help="chrF score using sacrebleu")
def chrf(
    target: str,
    reference: str,
    n_char_order: int = typer.Option(
        default=6,
        help=(
            "A character n-gram order. If n_char_order=6, the metrics refers to the "
            "official chrF/chrF++."
        ),
    ),
    n_word_order: int = typer.Option(
        default=2,
        help=(
            "A word n-gram order. If n_word_order=2, the metric refers to the official "
            "chrF++. If n_word_order=0, the metric is equivalent to the original ChrF."
        ),
    ),
    beta: float = typer.Option(
        default=2.0,
        help=(
            "Determines importance of recall w.r.t. precision. If beta=1, their "
            "importance is equal."
        ),
    ),
    **kwargs,
) -> float:
    """Calculate the chrF Score using Torchmetrics.

    Arguments:
        target: The target text.
        reference: The reference text.
        n_char_order: The character order.
        n_word_order: The word order.
        beta: The beta value.

    Returns:
        The chrF score.
    """
    score = sentence_chrf(
        target,
        [reference],
        char_order=n_char_order,
        word_order=n_word_order,
        beta=beta,
    )
    # Dividing by 100 to get the score in the range [0, 1]
    # sacrebleu gives the score in percentage
    return float(score.score) / 100.0
