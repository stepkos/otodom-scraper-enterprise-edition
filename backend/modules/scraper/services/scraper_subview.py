from typing import Iterator

from yarl import URL
from lxml import html

from modules.scraper.constants.parsing_rules import SUBPAGES_FIELD_MAP
from modules.scraper.utils import get_page


def datatable_xpath(aria_label: str) -> str:
    return f'//div[@data-testid="ad.top-information.table"]//div[@aria-label="{aria_label}"]/div[2]'


def extra_table_xpath(aria_label: str) -> str:
    return f'//div[@data-testid="ad.additional-information.table"]//div[@aria-label="{aria_label}"]/div[2]/div'


SUBVIEW_XPATHS = {
    "rent": datatable_xpath("Czynsz"),
    "max_floor": datatable_xpath("Piętro"),
    "energy_certificate": datatable_xpath("Certyfikat energetyczny"),
    "form_of_the_property": datatable_xpath("Forma własności"),
    "finishing_condition": datatable_xpath("Stan wykończenia"),
    "balcony_garden_terrace": datatable_xpath("Balkon / ogród / taras"),
    "parking_place": datatable_xpath("Miejsce parkingowe"),
    "heating": datatable_xpath("Ogrzewanie"),
    "description": '//div[@data-cy="adPageAdDescription"]',
    "market": extra_table_xpath("Rynek"),
    "advertisement_type": extra_table_xpath("Typ ogłoszeniodawcy"),
    "year_of_construction": extra_table_xpath("Rok budowy"),
    "type_of_development": extra_table_xpath("Rodzaj zabudowy"),
    "windows": extra_table_xpath("Okna"),
    "is_elevator": extra_table_xpath("Winda"),
}


def parse_single_attr_for_subview(elem: html.HtmlElement, attr_name: str):
    text = elem.xpath(SUBVIEW_XPATHS[attr_name])
    if text:
        result = SUBPAGES_FIELD_MAP[attr_name].process_value(text[0])
        if "Zapytaj" not in str(result):
            return result
    return None


def details_scraper_iterator(urls: Iterator[URL]):
    for url in urls:
        return details_scraper(html.fromstring(get_page(url)))


def details_scraper(page: html.HtmlElement):
    parse = lambda x: parse_single_attr_for_subview(page, x)
    return [
        parse("market"),
        parse("advertisement_type"),
        parse("year_of_construction"),
        parse("type_of_development"),
        parse("windows"),
        parse("is_elevator"),
        parse("max_floor"),
        parse("rent"),
        parse("energy_certificate"),
        parse("form_of_the_property"),
        parse("finishing_condition"),
        parse("balcony_garden_terrace"),
        parse("parking_place"),
        parse("heating"),
        parse("description"),
    ]


if __name__ == "__main__":
    print(
        details_scraper_iterator(
            [
                URL(
                    # "https://www.otodom.pl/pl/oferta/centrum-mieszkanie-z-potencjalem-najtaniej-ID4q9KH",
                    "https://www.otodom.pl/pl/oferta/mieszkanie-do-remontu-62-30-m2-ID4qJWE"
                ),
             ])
    )
