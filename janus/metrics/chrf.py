import typer
from torchmetrics.text import CHRFScore

from .metric import metric


@metric()
def chrf(
    src: str,
    dst: str,
    n_char_order: int = typer.Option(default=6),
    n_word_order: int = typer.Option(default=2),
    beta: float = typer.Option(default=2.0),
):
    """
    chrf metric
    :param src: src string to compare
    :param cmp: cmp string to compare
    :param n_char_order: character n gram order, default is 6
    :param n_word_order: word n n gram order, 0 = chrf, 2 = chrf++
    :param beta: importance of recall wrt precision, 1=equal importance
    """
    m = CHRFScore(
        n_char_order=n_char_order,
        n_word_order=n_word_order,
        beta=beta,
    )
    return float(m(src, dst).numpy())
