from functools import partial
from typing import Iterator

from yarl import URL
from lxml import html

from modules.apartments.models import Apartment, ApartmentDetails
from modules.scraper.constants.for_scraper import HTTP_HEADERS, SUBVIEW_XPATHS
from modules.scraper.constants.parsing_rules import SUBPAGES_FIELD_MAP
from modules.scraper.utils import get_page


def __parse_single_attr_for_subview(elem: html.HtmlElement, attr_name: str):
    text = elem.xpath(SUBVIEW_XPATHS[attr_name])
    if text:
        result = SUBPAGES_FIELD_MAP[attr_name].process_value(text[0])
        # TODO: Ten if jest do refaktoryzacji
        # ma to byc w parsing_rules
        # gdyby nie ten if to mozmey uzyc tej samej funkcji co w listview
        if "zapytaj" not in str(result).lower() and "brak informacji" not in str(result).lower():
            return result
    return None


def scrape_apartment_details(page: html.HtmlElement):
    parse = partial(__parse_single_attr_for_subview, page)
    return ApartmentDetails(
        market=parse("market"),
        advertisement_type=parse("advertisement_type"),
        year_of_construction=parse("year_of_construction"),
        type_of_development=parse("type_of_development"),
        windows=parse("windows"),
        is_elevator=parse("is_elevator"),
        max_floor=parse("max_floor"),
        rent=parse("rent"),
        energy_certificate=parse("energy_certificate"),
        form_of_the_property=parse("form_of_the_property"),
        finishing_condition=parse("finishing_condition"),
        balcony_garden_terrace=parse("balcony_garden_terrace"),
        parking_place=parse("parking_place"),
        heating=parse("heating"),
        description=parse("description")
    )


def scrape_apartments_details(urls: Iterator[URL]) -> Iterator[ApartmentDetails]:
    for url in urls:
        page = get_page(url)
        if page:
            yield scrape_apartment_details(html.fromstring(page))
        # TODO: Dodac obsluge bledow, nie tylko tutaj
        # Imo chyba już z requesta rzucajmy wyjatkami
        # obsluzy sie je w wyzszej warstwie
