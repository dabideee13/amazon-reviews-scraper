import time
import random
from typing import Optional, List, Dict
from itertools import chain
from pathlib import Path

from selectorlib import Extractor
import requests
import pandas as pd

extractor = Extractor.from_yaml_file('selectors.yml')


def scrape(url: str):
    """
    Source: https://www.scrapehero.com/how-to-scrape-amazon-product-reviews/
    """

    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print(f"Downloading {url}")
    r = requests.get(url, headers=headers)

    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None

    # Pass the HTML of the page and create
    return extractor.extract(r.text)


def crawl(url: str, n_pages: Optional[int] = None) -> List[Dict[str, str]]:

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


def format_reviews(data: List[Dict[str, str]]) -> pd.DataFrame:
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
