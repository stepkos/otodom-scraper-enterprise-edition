from typing import Iterable, Iterator

import requests
from yarl import URL

from modules.scrapers.constants.for_scraper_v2 import HTTP_HEADERS
from modules.scrapers.services.scraper_listview import NoMoreOffersException


def get_next_page_url(
    url: URL, param_name: str = "page", start: int = 1, step: int = 1, end=None
) -> URL:
    current_page = start
    if param_name in url.query:
        current_page = int(url.query[param_name])

    if end is not None and current_page > end:
        raise NoMoreOffersException("Artificial limit met")
    return url.update_query({param_name: current_page + step})


def url_paginator(
    url: URL, param_name: str = "page", start: int = 1, end: int | None = None
) -> Iterator[URL]:
    i = start
    if end is not None:
        while i <= end:
            yield url.update_query({param_name: i})
            i += 1
    else:
        while True:
            yield url.update_query({param_name: i})
            i += 1


def get_page(url: URL) -> str | None:
    """Get page content from provided URL.
    raises requests.RequestException if request failed."""
    response = requests.get(str(url), headers=HTTP_HEADERS)
    response.raise_for_status()
    return response.text


def pages_iterator(
    url: URL, param_name: str = "page", start: int = 1, end: int | None = None
) -> Iterator[str | None]:
    for url in url_paginator(url, param_name, start, end):
        yield get_page(url)


def subpages_iterator(urls: Iterable[URL]) -> Iterator[str | None]:
    yield from map(get_page, urls)
