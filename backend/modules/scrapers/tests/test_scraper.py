from unittest.mock import MagicMock, patch

from django.test import TestCase

from modules.apartments.constants import ApartmentStatus
from modules.apartments.models import Apartment
from modules.scrapers.models import ScraperSession
from modules.scrapers.services.custom_logger import CustomLogger
from modules.scrapers.services.scraper import ScraperService


class ScraperServiceTestCase(TestCase):
    def setUp(self):
        self.logger = MagicMock(spec=CustomLogger)
        self.service = ScraperService(self.logger)
        self.apartment = Apartment.objects.create(
            id=1, subpage="test-page", status=ApartmentStatus.WAITING_FOR_DETAILS
        )

    @patch("modules.scrapers.services.scraper.get_page")
    @patch("modules.scrapers.services.scraper.scrape_apartment_details")
    @patch("lxml.html.fromstring")
    def test_fetch_apartment_details(
        self, mock_fromstring, mock_scrape_details, mock_get_page
    ):
        mock_get_page.return_value = "<html></html>"
        mock_fromstring.return_value = MagicMock()
        mock_scrape_details.return_value = {"key": "value"}

        self.service.fetch_apartment_details(self.apartment)

        self.apartment.refresh_from_db()
        self.assertEqual(self.apartment.status, ApartmentStatus.SYNCHRONIZED)

    @patch("modules.scrapers.services.scraper.get_page")
    @patch("modules.scrapers.services.scraper.scrap_single_list_page")
    def test_fetch_apartments(self, mock_scrap_list_page, mock_get_page):
        session = ScraperSession.objects.create(id=1)
        url = "http://test-url.com"
        mails = ["test@example.com"]

        mock_get_page.return_value = "<html></html>"
        mock_scrap_list_page.return_value = [{"subpage": "test-subpage"}]

        result = self.service.fetch_apartments(session.id, url, mails)

        self.assertEqual(len(result), 2)
        self.logger.log_info.assert_called()
        self.assertTrue(session.apartments.filter(subpage="test-subpage").exists())
