HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 '
                  'Safari/537.3'
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
