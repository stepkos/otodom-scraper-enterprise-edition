import requests
from yarl import URL

from modules.scraper.constants import HTTP_HEADERS


def url_paginator(
    url: URL, param_name: str = 'page', start: int = 1, end: int | None = None
) -> URL:
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
    response = requests.get(str(url), headers=HTTP_HEADERS)
    if response.status_code == 200:
        return response.text
    return None
