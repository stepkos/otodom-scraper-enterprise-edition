from typing import Any

from yarl import URL

from modules.apartments.models import Apartment, ApartmentDetails
from modules.scraper.services.custom_logger import CustomLogger
from modules.scraper.services.scraper_listview import scrap_single_list_page
from modules.scraper.services.scraper_subview import scrape_apartment_details
from modules.scraper.tasks import fetch_apartment_details_task, DEFAULT_CELERY_DELAY_SECONDS, fetch_apartments_task
from modules.scraper.utils import get_next_page_url, get_page
from lxml import html


class ScraperService:
    def __init__(self, logger: CustomLogger):
        self.logger = logger

    def fetch_apartment_details(self, apartment: Apartment):
        url = apartment.get_abs_details_url()
        apart_details_data = scrape_apartment_details(html.fromstring(get_page(URL(url))))
        apart_details_data["apartment_id"] = apartment.id
        self._save_or_update(apart_details_data, "apartment_id", ApartmentDetails)
        return list(map(str, apart_details_data.items()))

    def fetch_apartments(self, url: str) -> URL | None:
        url = URL(url)
        try:
            for apart_data in scrap_single_list_page(page=get_page(url)):
                apartment = self._save_or_update(apart_data, "subpage", Apartment)
                self._schedule_details_task(apartment)

            self._schedule_next_page_task(url)

        except StopIteration:
            self.logger.log_info(f"Stop: No more pages to iterate")
            return None

    def _save_or_update(self, dict_data: dict, unique_key_name: str, ModelClass) -> Apartment | None:
        # try:
        apartment, created = ModelClass.objects.update_or_create(
            # TODO: check if this works as it should, cause I've struggled a bit
            **{unique_key_name: dict_data[unique_key_name]},
            defaults={
                key: value
                for key, value in dict_data.items()
                if key != unique_key_name
            },
        )
        if not created:
            self.logger.log_info(f"Updated: {dict_data}")
        else:
            self.logger.log_info(f"Created: {dict_data}")
        return apartment

    # except Exception as e:
    #     self.logger.log_error(f"Error processing {dict_data}: {e}")

    @staticmethod
    def _schedule_next_page_task(curr_url: URL):
        next_page_url = get_next_page_url(curr_url)
        fetch_apartments_task.apply_async(
            args=[str(next_page_url)],
            countdown=DEFAULT_CELERY_DELAY_SECONDS,
        )

    @staticmethod
    def _schedule_details_task(apartment: Apartment):
        fetch_apartment_details_task.apply_async(
            args=[apartment.id],
            countdown=DEFAULT_CELERY_DELAY_SECONDS,
        )
