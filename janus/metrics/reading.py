import re

import nltk
import readability
from nltk.tokenize import TweetTokenizer

from janus.metrics.metric import metric


def word_count(text):
    """Calculates word count exactly how readability package does

    Arguments:
        text: The input string.

    Returns:
        Word Count
    """
    tokenizer = TweetTokenizer()
    word_count = 0
    tokens = tokenizer.tokenize(text)
    for t in tokens:
        if not re.match(r"^[.,\/#!$%'\^&\*;:{}=\-_`~()]+$", t):
            word_count += 1
    return word_count


def _repeat_text(text):
    """Repeats a string until its length is over 100 words.

    Arguments:
        text: The input string.

    Returns:
        A string repeated to have more than 100 words.
    """
    # Strip to remove a newline
    text = text.strip()

    # Check if the text ends with a period
    if not text.endswith("."):
        text += "."  # Add a period if missing

    repeated_text = text

    while word_count(repeated_text) < 100:
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
    if not target.strip():  # Check if the target text is blank
        return None
    return get_readability(target).flesch().score


@metric(use_reference=False, help="The Flesch Grade Level Readability score")
def flesch_grade(target: str, **kwargs) -> float:
    """Calculate the Flesch Score using py-readability-metrics.

    Arguments:
        target: The target text.

    Returns:
        The Flesch-Kincaid Grade Level score.
    """
    if not target.strip():  # Check if the target text is blank
        return None
    return get_readability(target).flesch_kincaid().score


@metric(use_reference=False, help="The Gunning-Fog Readability score")
def gunning_fog(target: str, **kwargs) -> float:
    """Calculate the Gunning-Fog Score using py-readability-metrics.

    Arguments:
        target: The target text.

    Returns:
        The Gunning-Fog score.
    """
    if not target.strip():  # Check if the target text is blank
        return None
    return get_readability(target).gunning_fog().score


@metric(use_reference=False, help="The Gunning-Fog Grade Level Readability score")
def gunning_fog_grade(target: str, **kwargs) -> float:
    """Calculate the Gunning-Fog Grade Level Score using py-readability-metrics.

    Arguments:
        target: The target text.

    Returns:
        The Gunning-Fog Grade Level score.
    """
    if not target.strip():  # Check if the target text is blank
        return None
    grade_level = get_readability(target).gunning_fog().grade_level
    return None if grade_level == "na" else grade_level
