from .metric import metric


@metric()
def chrf(src, dst, alpha: float):
    return alpha
