def _subview_datatable_xpath(aria_label: str) -> str:
    return f'//div[@data-testid="ad.top-information.table"]//div[@aria-label="{aria_label}"]/div[2]'


def _subview_extra_table_xpath(aria_label: str) -> str:
    return f'//div[@data-testid="ad.additional-information.table"]//div[@aria-label="{aria_label}"]/div[2]/div'


HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/58.0.3029.110 "
    "Safari/537.3"
}

LISTVIEW_XPATHS = {
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

SUBVIEW_XPATHS = {
    "rent": _subview_datatable_xpath("Czynsz"),
    "max_floor": _subview_datatable_xpath("Piętro"),
    "energy_certificate": _subview_datatable_xpath("Certyfikat energetyczny"),
    "form_of_the_property": _subview_datatable_xpath("Forma własności"),
    "finishing_condition": _subview_datatable_xpath("Stan wykończenia"),
    "balcony_garden_terrace": _subview_datatable_xpath("Balkon / ogród / taras"),
    "parking_place": _subview_datatable_xpath("Miejsce parkingowe"),
    "heating": _subview_datatable_xpath("Ogrzewanie"),
    "description": '//div[@data-cy="adPageAdDescription"]',
    "market": _subview_extra_table_xpath("Rynek"),
    "advertisement_type": _subview_extra_table_xpath("Typ ogłoszeniodawcy"),
    "year_of_construction": _subview_extra_table_xpath("Rok budowy"),
    "type_of_development": _subview_extra_table_xpath("Rodzaj zabudowy"),
    "windows": _subview_extra_table_xpath("Okna"),
    "is_elevator": _subview_extra_table_xpath("Winda"),
    "exact_floors": _subview_datatable_xpath("Piętro"),
    "exact_rooms": _subview_datatable_xpath("Liczba pokoi"),
}
