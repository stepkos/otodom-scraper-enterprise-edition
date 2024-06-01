from functools import partial
from typing import Iterator

from yarl import URL
from lxml import html

from modules.apartments.models import Apartment
from modules.scraper.constants.for_scraper import LISTVIEW_XPATHS
from modules.scraper.utils import pages_iterator
from modules.scraper.constants.parsing_rules import FIELD_MAP


def parse_single_attr_for_list_view(elem: html.HtmlElement, attr_name: str):
    text = elem.xpath(LISTVIEW_XPATHS[attr_name])
    if text:
        return FIELD_MAP[attr_name].process_value(text[0])
    return None


def spec_list_apartments_iterator(page: html.HtmlElement) -> Iterator[Apartment]:
    for html_article in iter(page.xpath(LISTVIEW_XPATHS["offers"])):
        parse = partial(parse_single_attr_for_list_view, html_article)
        yield Apartment(
            price=parse("price"),
            title=parse("title"),
            subpage=parse("subpage"),
            rooms=parse("rooms"),
            area=parse("area"),
            floor=parse("floor"),
            address=parse("address"),
        )


def apartments_iterator(base_url: URL) -> Iterator[Apartment]:
    for page in pages_iterator(base_url):
        if page is None:
            raise ValueError("Failed to fetch page")
        tree = html.fromstring(page)
        if tree.xpath(LISTVIEW_XPATHS["offers-not-found"]):
            return
        yield from spec_list_apartments_iterator(tree)
