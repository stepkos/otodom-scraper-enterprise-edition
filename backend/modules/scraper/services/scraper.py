import requests
from yarl import URL
from lxml import html


class ListViewApartmentsIterator:
    XPATHS = {
        'offer': "//div[@class='css-136g1q2 e1tblfro0']"
    }

    def __init__(self, url: URL):
        self.url = url
        self.pages_iter = iter(pages_iterator(url))
        self.curr_page_text: str | None = None
        self.curr_page_tree: html.HtmlElement | None = None
        self.update_current_page()

    def update_current_page(self) -> None:
        page = next(self.pages_iter)
        if page is None:
            raise ValueError("Failed to fetch page")
        self.curr_page_text = page
        self.curr_page_tree = html.fromstring(page)
        # if nie ma wiecej ogloszen
        #     raise StopIteration

    def get_apartments(self):
        for offer in self.curr_page_tree.xpath(self.XPATHS['offer']):
            yield offer

    # def __next__(self):
    #     ...



class Scraper:
    def __init__(self, url: URL):
        self.url = url
