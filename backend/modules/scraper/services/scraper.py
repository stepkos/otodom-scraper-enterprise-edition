from django.db import IntegrityError
from yarl import URL

from modules.apartments.models import Apartment
from modules.scraper.services.custom_logger import CustomLogger
from modules.scraper.services.scraper_listview import scrap_single_list_page
from modules.scraper.utils import get_next_page_url, get_page


class ScraperService:
    def __init__(self, logger: CustomLogger):
        self.logger = logger

    def fetch_apartments(self, url: str) -> URL | None:
        url = URL(url)
        try:
            for apart_data in scrap_single_list_page(page=get_page(url)):
                try:
                    defaults = {
                        key: value
                        for key, value in apart_data.items()
                        if key != "subpage"
                    }
                    existing_apart, created = Apartment.objects.update_or_create(
                        # TODO: check if this works as it should, cause I've struggled a bit
                        subpage=apart_data["subpage"],
                        defaults=defaults,
                    )
                    if not created:
                        self.logger.log_info(f"Updated: {apart_data}")
                    else:
                        self.logger.log_info(f"Created: {apart_data}")
                except Exception as e:
                    self.logger.log_error(f"Error processing {apart_data}: {e}")
            return get_next_page_url(url)

        except StopIteration:
            self.logger.log_info(f"No more pages to iterate")
            return None
