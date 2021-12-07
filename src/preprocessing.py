from pathlib import Path
from typing import Union
import re

import pandas as pd
from nltk import pos_tag, word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from tools import read_json, pipe

vds = SentimentIntensityAnalyzer()


def format_rating(rating: str) -> Union[float, None]:
    try:
        rate = rating.split()[0]
        return eval(rate)
    except (AttributeError, IndexError):
        pass


def label_sentiment(text: str, mode: str = 'string') -> int:
    """Labels a given text with its equivalent sentiment using `vader`.

    Args:
        text (str): A string, could be a single word, sentence, or paragraph.
        mode (str, optional): Possible choices could be `string` or `integer`. Defaults to 'string'.

    Returns:
        int: The sentiment of the text either encoded as string or integer.
    """
    labels = read_json(Path.cwd(), filename='labels.json')[mode]

    sentiment_stats = vds.polarity_scores(text)
    sentiment = sentiment_stats['compound']

    if sentiment >= 0.05:
        return labels['positive']
    elif (sentiment > -0.05) and (sentiment < 0.05):
        return labels['neutral']
    else:
        return labels['negative']


def remove_stopwords(tokens: str) -> list[str]:
    stop_words = set(stopwords.words('english') + ["can\'t"])
    return [word for word in tokens if not word in stop_words]


def remove_possessive(text: str) -> str:
    pattern = r"(\'s)"
    return re.sub(pattern, "", text).strip()


def remove_punctuations(text: str) -> str:
    pattern = r"[^\w\s]"
    return re.sub(pattern, "", text).strip()


def remove_doublespace(text: str) -> str:
    pattern = r" +"
    return re.sub(pattern, " ", text).strip()


def remove_single(text: str) -> str:
    pattern = r"\b[a-zA-Z]\b"
    return re.sub(pattern, "", text)


def remove_specific(text: str) -> str:
    pattern = r"nt"
    return re.sub(pattern, "", text)


def clean_text(text: str) -> str:
    return pipe(
        text,
        remove_punctuations,
        remove_single,
        remove_specific,
        remove_doublespace
    )


def get_speech(text: str, part_of_speech: str) -> list[str]:
    return [x for (x, y) in pos_tag(text.split()) if y in (part_of_speech)]


if __name__ == "__main__":

    df = pd.read_csv(data_path('keychron_K2_reveiws.csv'))
    df['sentiment'] = df.content.apply(label_sentiment)
