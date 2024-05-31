from typing import Iterator

from yarl import URL
from lxml import html

from modules.scraper.services.parsing_rules import FIELD_MAP
from modules.apartments.models import Apartment
from modules.scraper.utils import pages_iterator

XPATHS = {
    "offers-not-found": "//div[@data-cy='no-search-results']",
    "offers": "//div[@data-cy='search.listing.organic' or @data-cy='search.listing.promoted']/ul/li/article",
    "price": ".//div[@data-testid='listing-item-header']/span",
    "title": ".//a[@data-cy='listing-item-link']/p",
    "subpage": ".//a[@data-cy='listing-item-link']",
    "rooms": ".//dt[text()='Liczba pokoi']/following-sibling::dd",
    "area": ".//dt[text()='Powierzchnia']/following-sibling::dd",
    "floor": ".//dt[text()='Piętro']/following-sibling::dd",
    "address": ".//p[@data-testid='advert-card-address']",
}


def spec_list_apartments_iterator(page: html.HtmlElement):
    for html_article in iter(page.xpath(XPATHS["offers"])):
        def parse_single_attr(attr_name: str):
            text = html_article.xpath(XPATHS[attr_name])
            if text:
                return FIELD_MAP[attr_name].process_value(text[0])
            return None

        yield Apartment(
            price=parse_single_attr("price"),
            title=parse_single_attr("title"),
            subpage=parse_single_attr("subpage"),
            rooms=parse_single_attr("rooms"),
            area=parse_single_attr("area"),
            floor=parse_single_attr("floor"),
            address=parse_single_attr("address"),
        )


def apartments_iterator(base_url: URL) -> Iterator:
    for page in pages_iterator(base_url):
        if page is None:
            raise ValueError("Failed to fetch page")
        tree = html.fromstring(page)
        if tree.xpath(XPATHS["offers-not-found"]):
            return
        yield from spec_list_apartments_iterator(tree)


class ScraperService:
    def __init__(self, url: str):
        self.url = URL(url)
