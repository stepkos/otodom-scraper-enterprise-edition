from yarl import URL
from lxml import html

from modules.scraper.services.parsing_rules import FIELD_MAP
# from modules.apartments.models import Apartment
from modules.scraper.utils import pages_iterator



class SpecListApartmentsIterator:

    def __init__(self, page: html.HtmlElement):
        self.page = page
        self.apartments_iter = iter(page.xpath(XPATHS["offers"]))

    def __next__(self):
        html_article = next(self.apartments_iter)
        return self.parser(html_article)

    def __iter__(self):
        return self

    def parser(self, html_article: html.HtmlElement):
        def parse_single_attr(attr_name: str):
            text = html_article.xpath(XPATHS[attr_name])
            if text:
                return FIELD_MAP[attr_name].process_value(text[0])
            return None

        # return Apartment(
        #     price=parse_single_attr("price"),
        #     title=parse_single_attr("title"),
        #     subpage=parse_single_attr("subpage"),
        #     rooms=parse_single_attr("rooms"),
        #     area=parse_single_attr("area"),
        #     floor=parse_single_attr("floor"),
        #     address=parse_single_attr("address"),
        # )
        return [
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
        yield from SpecListApartmentsIterator(curr_tree)


class Scraper:
    def __init__(self, url: URL):
        self.url = url


if __name__ == "__main__":
    turl = URL(
        "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/dolnoslaskie?limit=36&ownerTypeSingleSelect=ALL&priceMin=123&priceMax=100000&by=DEFAULT&direction=DESC&viewType=listing"
    )
    for x in apartments_iterator(turl):
        print(x)
