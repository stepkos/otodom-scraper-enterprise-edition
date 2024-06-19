def _subview_datatable_xpath(keyword: str) -> str:
    return '//h4[text()="Mieszkanie na sprzedaż"]/following-sibling::div[2]/div/p[contains(., "' + keyword + '")]/following-sibling::p'


def _subview_extra_table_xpath(keyword: str) -> str:
    return '//h4[text()="Mieszkanie na sprzedaż"]/following-sibling::div[3]/div[1]//p[contains(., "' + keyword + '")]/following-sibling::p'


HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 "
                  "Safari/537.3"
}

LISTVIEW_XPATHS = {
    "offers-not-found": "//div[@data-cy='no-search-results']",
    "offers": "//div[@data-cy='search.listing.organic' or @data-cy='search.listing.promoted']/ul/li/article",
    "price": ".//a[@data-cy='listing-item-link']/preceding-sibling::div/span",
    "title": ".//a[@data-cy='listing-item-link']/p",
    "subpage": ".//a[@data-cy='listing-item-link']",
    "rooms": ".//dt[text()='Liczba pokoi']/following-sibling::dd",
    "area": ".//dt[text()='Powierzchnia']/following-sibling::dd",
    "floor": ".//dt[text()='Piętro']/following-sibling::dd",
    "address": ".//a[@data-cy='listing-item-link']/following-sibling::div/p",
}

SUBVIEW_XPATHS = {
    "rent": _subview_datatable_xpath("Czynsz"),
    "max_floor": _subview_datatable_xpath("Piętro"),
    "energy_certificate": _subview_datatable_xpath("Certyfikat energetyczny"),
    "form_of_the_property": _subview_datatable_xpath("Forma własności"),
    "finishing_condition": _subview_datatable_xpath("Stan wykończenia"),
    "balcony_garden_terrace": _subview_datatable_xpath("Balkon / ogród / taras"),  # THIS NO LONGER EXISTS
    "parking_place": _subview_datatable_xpath("Miejsce parkingowe"),  # THIS NO LONGER EXISTS
    "heating": _subview_datatable_xpath("Ogrzewanie"),  # THIS NO LONGER EXISTS
    "description": '//div[@data-cy="adPageAdDescription"]',
    "market": _subview_extra_table_xpath("Rynek"),
    "advertisement_type": _subview_extra_table_xpath("Typ ogłoszeniodawcy"),
    "year_of_construction": _subview_extra_table_xpath("Rok budowy"),
    "type_of_development": _subview_extra_table_xpath("Rodzaj zabudowy"),
    "windows": _subview_extra_table_xpath("Okna"),
    "is_elevator": _subview_extra_table_xpath("Winda"),
    "exact_floors": _subview_datatable_xpath("Piętro"),
    "exact_rooms": "//button[.//div[contains(text(), 'pokoje')]]/div[2]'",
}
