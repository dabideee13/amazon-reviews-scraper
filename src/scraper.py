from typing import Optional
from pathlib import Path
import time
import random
from itertools import chain

from selectorlib import Extractor
import requests
import pandas as pd

from tools import read_header

extractor = Extractor.from_yaml_file('selectors.yml')

HEADERS = read_header()


def _download_page(url: str, headers: dict[str, str] = HEADERS):

    # Download the page using requests
    print(f"Downloading {url}")
    request = requests.get(url, headers=headers)

    # Simple check to check if page was blocked (Usually 503)
    if request.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in request.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, request.status_code))
        return None

    return request


def scrape(url: str, headers: dict[str, str] = HEADERS) -> dict[str, str]:
    """
    Source: https://www.scrapehero.com/how-to-scrape-amazon-product-reviews/
    """

    request = _download_page(url, headers=headers)
    return extractor.extract(request.text)


def crawl(url: str, n_pages: Optional[int] = None) -> list[dict[str, str]]:

    scrape(url)

    if n_pages is None:
        n_pages = float('inf')

    all_data = []

    counter = 0
    while counter < n_pages:

        try:
            data = scrape(url)
            time.sleep(random.randint(2, 10))
            all_data.append(data)

            pre_url = "https://www.amazon.com"
            url = pre_url + data['next_page']

            counter += 1

        except (KeyboardInterrupt, Exception):
            break

    return all_data


def format_reviews(data: list[dict[str, str]]) -> pd.DataFrame:
    all_reviews = [review['reviews'] for review in data]
    return pd.DataFrame(list(chain(*all_reviews)))


if __name__ == '__main__':

    URL = "https://www.amazon.com/Keychron-Wireless-Bluetooth-Mechanical-Keyboard/product-reviews/B07YB32H52/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

    # Scrape all reviews from all available pages
    data = crawl(URL)

    # Convert data to DataFrame
    df = format_reviews(data)

    # Export data to csv
    data_path = lambda filename: Path.joinpath(Path.cwd(), 'data', filename)
    df.to_csv(data_path('keychron_K2_reviews.csv'))
