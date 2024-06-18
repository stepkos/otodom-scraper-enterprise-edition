from celery.utils.log import get_task_logger
from modules.apartments.models import Apartment
from modules.core.utils import celery_task
from modules.scraper.services.custom_logger import CustomLogger
from modules.scraper.services.scraper import ScraperService

celery_logger = get_task_logger(__name__)


@celery_task
def fetch_apartment_details_task(self, apartment: Apartment):
    # create details or update if exists
    ...


@celery_task
def fetch_apartments_task(_, url: str):
    logger = CustomLogger(celery_logger)
    next_page_url = ScraperService(logger).fetch_apartments(url)
    if next_page_url is not None:
        fetch_apartments_task.apply_async(
            args=[str(next_page_url)],
            countdown=3,  # run next in 3 sec
        )
    return logger.get_result_dict()
