import unittest
from unittest.mock import MagicMock, patch

from requests.exceptions import RequestException
from yarl import URL

from modules.scrapers.constants.for_scraper_v2 import HTTP_HEADERS
from modules.scrapers.services.scraper_listview import NoMoreOffersException
from modules.scrapers.utils import (
    get_next_page_url,
    get_page,
    pages_iterator,
    subpages_iterator,
    url_paginator,
)


class ScraperUtilsTestCase(unittest.TestCase):

    def test_get_next_page_url(self):
        url = URL("http://example.com/?page=1")
        next_url = get_next_page_url(url)
        self.assertEqual(str(next_url), "http://example.com/?page=2")

        next_url = get_next_page_url(url, step=2)
        self.assertEqual(str(next_url), "http://example.com/?page=3")

        with self.assertRaises(NoMoreOffersException):
            get_next_page_url(get_next_page_url(url, end=1), end=1)

    def test_url_paginator(self):
        url = URL("http://example.com")
        paginator = url_paginator(url, start=1, end=3)
        paginated_urls = list(paginator)
        expected_urls = [
            "http://example.com/?page=1",
            "http://example.com/?page=2",
            "http://example.com/?page=3",
        ]
        self.assertEqual([str(u) for u in paginated_urls], expected_urls)

    @patch("requests.get")
    def test_get_page(self, mock_get):
        url = URL("http://example.com")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "page content"
        mock_get.return_value = mock_response

        content = get_page(url)
        self.assertEqual(content, "page content")
        mock_get.assert_called_once_with(str(url), headers=HTTP_HEADERS)

        mock_get.side_effect = RequestException
        with self.assertRaises(RequestException):
            get_page(url)

    @patch("modules.scrapers.utils.get_page")
    def test_pages_iterator(self, mock_get_page):
        url = URL("http://example.com")
        mock_get_page.side_effect = ["page 1", "page 2", "page 3"]

        pages = list(pages_iterator(url, start=1, end=3))
        self.assertEqual(pages, ["page 1", "page 2", "page 3"])

    @patch("modules.scrapers.utils.get_page")
    def test_subpages_iterator(self, mock_get_page):
        urls = [URL(f"http://example.com/?page={i}") for i in range(1, 4)]
        mock_get_page.side_effect = ["page 1", "page 2", "page 3"]

        pages = list(subpages_iterator(urls))
        self.assertEqual(pages, ["page 1", "page 2", "page 3"])
