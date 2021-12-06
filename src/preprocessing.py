from pathlib import Path
from typing import Union
import json

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from tools import read_json

vds = SentimentIntensityAnalyzer()


def format_rating(rating: str) -> Union[float, None]:
    try:
        rate = rating.split()[0]
        return eval(rate)
    except (AttributeError, IndexError):
        pass


def label_sentiment(text: str, mode: str = 'string') -> int:
    """[summary]

    Args:
        text (str): [description]
        mode (str, optional): Possible choices could be `string` or `integer`. Defaults to 'string'.

    Returns:
        int: [description]
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


if __name__ == "__main__":

    data_path = lambda filename: Path.joinpath(Path.cwd(), 'data', filename)
    df = pd.read_csv(data_path('keychron_K2_reveiws.csv'))
    df['sentiment'] = df.content.apply(label_sentiment)


# TODO: perform proper preprocessing
# TODO: do most frequent occurences
# TODO: find relationships with other features, if any