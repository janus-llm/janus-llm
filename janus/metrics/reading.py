import nltk
import readability

from .metric import metric


def get_readability(target: str) -> readability.Readability:
    """Create a Readability object from an input string

    Arguments:
        target: The target text.

    Returns:
        py-readability-metrics Readability object for that text
    """
    nltk.download("punkt", quiet=True)
    return readability.Readability(target)


@metric(use_reference=False, help="The Flesch Readability score")
def flesch(target: str, **kwargs) -> float:
    """Calculate the Flesch Score using py-readability-metrics.

    Arguments:
        target: The target text.

    Returns:
        The Flesch score.
    """

    return get_readability(target).flesch().score


@metric(use_reference=False, help="The Gunning-Fog Readability score")
def gunning_fog(target: str, **kwargs) -> float:
    """Calculate the Gunning-Fog Score using py-readability-metrics.

    Arguments:
        target: The target text.

    Returns:
        The Gunning-Fog score.
    """

    return get_readability(target).gunning_fog().score
