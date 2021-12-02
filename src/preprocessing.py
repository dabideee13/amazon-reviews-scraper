from pathlib import Path

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

vds = SentimentIntensityAnalyzer()


def label_sentiment(text: str) -> int:
    sentiment_stats = vds.polarity_scores(text)
    sentiment = sentiment_stats['compound']

    if sentiment >= 0.05:
        return 1
    elif (sentiment > -0.05) and (sentiment < 0.05):
        return 0
    else:
        return -1


if __name__ == "__main__":

    data_path = lambda filename: Path.joinpath(Path.cwd(), 'data', filename)
    df = pd.read_csv(data_path('keychron_K2_reveiws.csv'))
    df['sentiment'] = df.content.apply(label_sentiment)


# TODO: perform proper preprocessing
# TODO: do most frequent occurences
# TODO: find relationships with other features, if any