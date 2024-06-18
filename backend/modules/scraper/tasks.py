from celery.utils.log import get_task_logger

from modules.apartments.models import Apartment
from modules.core.utils import celery_task
from modules.scraper.services.custom_logger import CustomLogger

celery_logger = get_task_logger(__name__)

DEFAULT_CELERY_DELAY_SECONDS = 10


@celery_task
def fetch_apartment_details_task(_, apartment_id):
    print(apartment_id)
    from modules.scraper.services.scraper import ScraperService

    apartment = Apartment.objects.get(id=apartment_id)
    celery_logger.info(apartment_id)
    logger = CustomLogger(celery_logger)
    ScraperService(logger).fetch_apartment_details(apartment)
    return logger.get_result_dict()


@celery_task
def fetch_apartments_task(_, url: str):
    from modules.scraper.services.scraper import ScraperService

    logger = CustomLogger(celery_logger)
    ScraperService(logger).fetch_apartments(url)
    return logger.get_result_dict()
