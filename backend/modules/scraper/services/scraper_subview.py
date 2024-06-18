from datetime import datetime
from functools import partial
from typing import Iterator

from lxml import html
from modules.apartments.models import ApartmentDetails
from modules.scraper.constants.for_scraper import SUBVIEW_XPATHS
from modules.scraper.constants.parsing_rules import SUBPAGES_FIELD_MAP
from modules.scraper.services.scraper_listview import parse_single_attr
from modules.scraper.utils import get_page
from yarl import URL


def scrape_apartment_details(page: html.HtmlElement):
    parse = partial(parse_single_attr, SUBVIEW_XPATHS, SUBPAGES_FIELD_MAP, page)
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
        description=parse("description"),
    )


def scrape_apartments_details(urls: Iterator[URL]) -> Iterator[ApartmentDetails]:
    for url in urls:
        page = get_page(url)
        if page:
            yield scrape_apartment_details(html.fromstring(page))
        # TODO: Dodac obsluge bledow, nie tylko tutaj
        # Imo chyba już z requesta rzucajmy wyjatkami
        # obsluzy sie je w wyzszej warstwie
