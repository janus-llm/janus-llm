import typer
from torchmetrics.text import CHRFScore

from .metric import metric


@metric(help="chrF Score using Torchmetrics")
def chrf(
    src: str,
    dst: str,
    n_char_order: int = typer.Option(default=6),
    n_word_order: int = typer.Option(default=2),
    beta: float = typer.Option(default=2.0),
):
    """Calculate the chrF Score using Torchmetrics.

    Arguments:
        src: The source text.
        dst: The destination text.
        n_char_order: The character order.
        n_word_order: The word order.
        beta: The beta value.

    Returns:
        The chrF score.
    """
    m = CHRFScore(
        n_char_order=n_char_order,
        n_word_order=n_word_order,
        beta=beta,
    )
    return float(m(src, dst).numpy())
