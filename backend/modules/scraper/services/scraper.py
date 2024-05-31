from itertools import count
from typing import Iterator

from yarl import URL
from lxml import html

from modules.scraper.services.parsing_rules import FIELD_MAP
# from modules.apartments.models import Apartment
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

        # yield Apartment(
        #     price=parse_single_attr("price"),
        #     title=parse_single_attr("title"),
        #     subpage=parse_single_attr("subpage"),
        #     rooms=parse_single_attr("rooms"),
        #     area=parse_single_attr("area"),
        #     floor=parse_single_attr("floor"),
        #     address=parse_single_attr("address"),
        # )
        yield [
            parse_single_attr("price"),
            parse_single_attr("title"),
            parse_single_attr("subpage"),
            parse_single_attr("rooms"),
            parse_single_attr("area"),
            parse_single_attr("floor"),
            parse_single_attr("address"),
        ]


def apartments_iterator(base_url: URL) -> Iterator:
    def __get_apartments_tree(page) -> html.HtmlElement:
        if page is None:
            raise ValueError("Failed to fetch page")
        tree = html.fromstring(page)
        if tree.xpath(XPATHS["offers-not-found"]):
            raise StopIteration
        return tree

    for curr_page in pages_iterator(base_url):
        curr_tree = __get_apartments_tree(curr_page)
        yield from spec_list_apartments_iterator(curr_tree)


class ScraperService:
    def __init__(self, url: str):
        self.url = URL(url)


if __name__ == "__main__":
    turl = URL(
        "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie?limit=36&ownerTypeSingleSelect=ALL&priceMin=123&priceMax=100000&by=DEFAULT&direction=DESC&viewType=listing"
    )
    for x in apartments_iterator(turl):
        print(x)
