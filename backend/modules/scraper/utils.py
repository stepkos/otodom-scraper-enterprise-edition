import requests
from yarl import URL

from modules.scraper.constants import HTTP_HEADERS


def url_paginator(
    url: URL, param_name: str = 'page', start: int = 1, end: int | None = None
) -> Iterator[URL]:
    i = start
    if end is not None:
        while i <= end:
            yield url.with_query({param_name: i})
            i += 1
    else:
        while True:
            yield url.with_query({param_name: i})
            i += 1


def get_page(url: URL) -> str | None:
    """Get page content from provided URL.
    None is returned if request failed."""
    response = requests.get(str(url), headers=HTTP_HEADERS)
    if response.status_code == 200:
        return response.text
    # TODO log error
    return None


def pages_iterator(
    url: URL, param_name: str = 'page', start: int = 1, end: int | None = None
) -> str | None:
    for i in url_paginator(url, param_name, start, end):
        yield get_page(i)
