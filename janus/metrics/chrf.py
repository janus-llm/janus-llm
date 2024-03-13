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
    m = CHRFScore(
        n_char_order=n_char_order,
        n_word_order=n_word_order,
        beta=beta,
    )
    return float(m(src, dst).numpy())
