import requests
from yarl import URL


class ListViewApartmentsIterator:
    def __init__(self, url: URL):
        self.url = url

    def __next__(self):
        return ...


class Scraper:
    def __init__(self, url: URL):
        self.url = url
