from functools import partial
from typing import Iterator

from lxml import html

from modules.apartments.models import ApartmentStatus
from modules.scrapers.constants.for_scraper_v2 import LISTVIEW_XPATHS
from modules.scrapers.constants.parsing_rules import FIELD_MAP
from modules.scrapers.services.parsing_processors import parse_single_attr


def spec_list_apartments_iterator(page: html.HtmlElement) -> Iterator[dict]:
    for html_article in iter(page.xpath(LISTVIEW_XPATHS["offers"])):
        parse = partial(parse_single_attr, LISTVIEW_XPATHS, FIELD_MAP, html_article)
        yield {
            "price": parse("price"),
            "title": parse("title"),
            "subpage": parse("subpage"),
            "rooms": parse("rooms"),
            "area": parse("area"),
            "floor": parse("floor"),
            "address": parse("address"),
            "status": ApartmentStatus.WAITING_FOR_DETAILS,
        }


# def apartments_iterator(base_url: URL, page_delay=2) -> Iterator[Apartment]:
#     for page in pages_iterator(base_url):
#         if page is None:
#             raise ValueError("Failed to fetch page")
#         yield from scrap_single_list_page(page)
#         sleep(page_delay)


def scrap_single_list_page(page: str) -> Iterator[dict]:
    tree = html.fromstring(page)
    if tree.xpath(LISTVIEW_XPATHS["offers-not-found"]):
        raise NoMoreOffersException("No more offers")
    yield from spec_list_apartments_iterator(tree)


class NoMoreOffersException(Exception):
    def __init__(self, message):
        super().__init__(message)
