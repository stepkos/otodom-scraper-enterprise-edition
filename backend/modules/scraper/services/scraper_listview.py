from functools import partial
from time import sleep
from typing import Iterator

from lxml import html
from yarl import URL

from modules.apartments.models import Apartment, ApartmentStatus
from modules.scraper.constants.for_scraper import LISTVIEW_XPATHS
from modules.scraper.constants.parsing_rules import FIELD_MAP
from modules.scraper.services.parsing_processors import ProcessorDict
from modules.scraper.utils import pages_iterator


def parse_single_attr(
    xpaths_dict: dict[str, str],
    parse_dict: ProcessorDict,
    elem: html.HtmlElement,
    attr_name: str,
):
    if text := elem.xpath(xpaths_dict[attr_name]):
        return parse_dict[attr_name].process_value(text[0])


def spec_list_apartments_iterator(page: html.HtmlElement) -> Iterator[Apartment]:
    for html_article in iter(page.xpath(LISTVIEW_XPATHS["offers"])):
        parse = partial(parse_single_attr, LISTVIEW_XPATHS, FIELD_MAP, html_article)
        yield Apartment(
            price=parse("price"),
            title=parse("title"),
            subpage=parse("subpage"),
            rooms=parse("rooms"),
            area=parse("area"),
            floor=parse("floor"),
            address=parse("address"),
            status=ApartmentStatus.WAITING_FOR_DETAILS,
        )


def apartments_iterator(base_url: URL, page_delay=2) -> Iterator[Apartment]:
    for page in pages_iterator(base_url):
        if page is None:
            raise ValueError("Failed to fetch page")
        tree = html.fromstring(page)
        if tree.xpath(LISTVIEW_XPATHS["offers-not-found"]):
            return
        yield from spec_list_apartments_iterator(tree)
        sleep(page_delay)
