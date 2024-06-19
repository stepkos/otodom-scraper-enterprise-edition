from celery import chain, group

from modules.apartments.models import Apartment
from modules.core.utils import celery_task
from modules.emails.tasks import test_mail
from modules.scrapers.services.custom_logger import CustomLogger, celery_logger

DEFAULT_CELERY_DELAY_SECONDS = 10


@celery_task
def fetch_apartment_details_task(logger: CustomLogger, _, apartment_id):
    from modules.scrapers.services.scraper import ScraperService

    apartment = Apartment.objects.get(id=apartment_id)
    return ScraperService(logger).fetch_apartment_details(apartment)


@celery_task
def fetch_apartments_task(logger: CustomLogger, _, url: str):
    from modules.scrapers.services.scraper import ScraperService

    subtasks = ScraperService(logger).fetch_apartments(url)
    return group(subtasks) if subtasks else None


@celery_task
def scraper_master_task(__, _, url: str):
    chain(fetch_apartments_task.s(url) | handle_tasks_done.s()).delay()


@celery_task
def handle_tasks_done(logger: CustomLogger, _, result):
    logger.log_info("result")
    logger.log_error("All tasks are done!")
    test_mail.delay("szymon@kowalinski.dev")
    return result
