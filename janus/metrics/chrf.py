from torchmetrics.text import CHRFScore

from .metric import metric


@metric()
def chrf(src, dst, alpha: float):
    m = CHRFScore()
    return m(src, dst).numpy()
