from celery import chain

import requests
from lxml import html
from yarl import URL

from modules.apartments.constants import ApartmentStatus
from modules.apartments.models import Apartment, ApartmentDetails
from modules.scrapers.models import ScraperSession
from modules.scrapers.services.custom_logger import CustomLogger
from modules.scrapers.services.scraper_listview import (
    NoMoreOffersException,
    scrap_single_list_page,
)
from modules.scrapers.services.scraper_subview import scrape_apartment_details
from modules.scrapers.tasks import fetch_apartment_details_task, fetch_apartments_task, handle_tasks_done, valuate_task
from modules.scrapers.utils import get_next_page_url, get_page


class ScraperService:
    def __init__(self, logger: CustomLogger):
        self.logger = logger

    def fetch_apartment_details(self, apartment: Apartment):
        apart_details_data = {}
        try:
            url = apartment.get_abs_details_url()
            apart_details_data = scrape_apartment_details(
                html.fromstring(get_page(URL(url)))
            )
            apart_details_data["apartment_id"] = apartment.id
            self._save_or_update(apart_details_data, "apartment_id", ApartmentDetails)

            apartment.status = ApartmentStatus.SYNCHRONIZED
            apartment.save()

        except requests.RequestException:
            apartment.status = ApartmentStatus.DELETED
            apartment.save()

        return list(map(str, apart_details_data.items()))

    def fetch_apartments(self, session_id, url: str, mails: list[str]):
        session = ScraperSession.objects.get(id=session_id)
        url = URL(url)
        try:
            subtasks = []
            for apart_data in scrap_single_list_page(page=get_page(url)):
                apartment = self._save_or_update(apart_data, "subpage", Apartment)
                session.apartments.add(apartment)
                subtasks.append(chain(
                    self._get_signature_details_task(apartment),
                    self._get_valuate_task(apartment),
                )
                )
            session.save()
            subtasks.append(self._get_signature_next_page_task(session_id, url, mails))
            return subtasks
        except NoMoreOffersException:
            self.logger.log_info(f"Stop: No more pages to iterate")
            return [handle_tasks_done.s(session_id, mails)]

    def _save_or_update(
            self, dict_data: dict, unique_key_name: str, ModelClass
    ) -> Apartment | None:
        try:
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

        except Exception as e:
            self.logger.log_error(f"Error processing {dict_data}: {e}")

    @staticmethod
    def _get_signature_next_page_task(session_id, curr_url: URL, mails: list[str]):
        next_page_url = get_next_page_url(curr_url)
        return fetch_apartments_task.s(session_id, str(next_page_url), mails)

    @staticmethod
    def _get_signature_details_task(apartment: Apartment):
        return fetch_apartment_details_task.s(apartment.id)

    @staticmethod
    def _get_valuate_task(apartment: Apartment):
        return valuate_task.s(apartment.id)
