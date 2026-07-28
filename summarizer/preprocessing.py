import re
from nltk.tokenize import sent_tokenize


def clean_text(text):
    """
    Remove extra whitespace and blank lines.
    """
    return re.sub(r"\s+", " ", text).strip()


def split_into_sentences(text):
    """
    Split text into sentences.
    """
    return sent_tokenize(clean_text(text))


def word_count(text):
    """
    Count the number of words in the cleaned text.
    """
    return len(clean_text(text).split())


def sentence_count(text):
    """
    Count the number of sentences in the text.
    """
    return len(split_into_sentences(text))