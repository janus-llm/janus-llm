import nltk
import readability

from .metric import metric


def _repeat_text(text):
    """Repeats a string until its length is over 100 words.

    Arguments:
        text: The input string.

    Returns:
        A string repeated to have more than 100 words.
    """

    # Check if repeated text is long enough, repeat more if needed
    repeated_text = text
    while len(repeated_text.split()) < 100:
        repeated_text += " " + text

    return repeated_text


def get_readability(target: str) -> readability.Readability:
    """Create a Readability object from an input string

    Arguments:
        target: The target text.

    Returns:
        py-readability-metrics Readability object for that text
    """
    nltk.download("punkt", quiet=True)
    target = _repeat_text(target)
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
