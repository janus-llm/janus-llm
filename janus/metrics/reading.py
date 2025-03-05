import re

from nltk.tokenize import TweetTokenizer
from textstat import textstat

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


@metric(use_reference=False, help="The Flesch Readability score")
def flesch(target: str, **kwargs) -> float:
    """Calculate the Flesch Score using textstat.

    Arguments:
        target: The target text.

    Returns:
        The Flesch score.
    """
    if not target.strip():  # Check if the target text is blank
        return None
    target = _repeat_text(target)
    return textstat.flesch_reading_ease(target)


@metric(use_reference=False, help="The Flesch Grade Level Readability score")
def flesch_grade(target: str, **kwargs) -> float:
    """Calculate the Flesch Score using textstat.

    Arguments:
        target: The target text.

    Returns:
        The Flesch-Kincaid Grade Level score.
    """
    if not target.strip():  # Check if the target text is blank
        return None
    target = _repeat_text(target)
    return textstat.flesch_kincaid_grade(target)


@metric(use_reference=False, help="The Gunning-Fog Readability score")
def gunning_fog(target: str, **kwargs) -> float:
    """Calculate the Gunning-Fog Score using textstat.

    Arguments:
        target: The target text.

    Returns:
        The Gunning-Fog score.
    """
    if not target.strip():  # Check if the target text is blank
        return None
    target = _repeat_text(target)
    return textstat.gunning_fog(target)


@metric(use_reference=False, help="The Dale-Chall Readability score")
def dale_chall(target: str, **kwargs) -> float:
    """Calculate the Dale-Chall Readability Score using textstat.

    Arguments:
        target: The target text.

    Returns:
        The Dale-Chall score.
    """
    if not target.strip():  # Check if the target text is blank
        return None
    target = _repeat_text(target)
    return textstat.dale_chall_readability_score_v2(target)


@metric(use_reference=False, help="The Automated Readability Index")
def automated_readability(target: str, **kwargs) -> float:
    """Calculate the Automated Readability Index using textstat.

    Arguments:
        target: The target text.

    Returns:
        The Automated Readability score.
    """
    if not target.strip():  # Check if the target text is blank
        return None
    target = _repeat_text(target)
    return textstat.automated_readability_index(target)


@metric(use_reference=False, help="The Coleman-Liau Index")
def coleman_liau(target: str, **kwargs) -> float:
    """Calculate the Coleman-Liau Index using textstat.

    Arguments:
        target: The target text.

    Returns:
        The Coleman-Liau Index.
    """
    if not target.strip():  # Check if the target text is blank
        return None
    target = _repeat_text(target)
    return textstat.coleman_liau_index(target)
