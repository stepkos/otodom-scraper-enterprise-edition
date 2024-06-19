from itertools import chain
from random import random

from celery import chord, group

from modules.apartments.constants import ApartmentStatus
from modules.apartments.models import Apartment
from modules.core.utils import celery_task, flatten
from modules.emails.tasks import test_mail
from modules.scrapers.services.custom_logger import CustomLogger


@celery_task
def fetch_apartment_details_task(logger: CustomLogger, _, apartment_id):
    from modules.scrapers.services.scraper import ScraperService

    apartment = Apartment.objects.get(id=apartment_id)
    return ScraperService(logger).fetch_apartment_details(apartment)


@celery_task
def valuate_task(__, _, result, apartment_id):
    __.log_error("XD: " + str(result))
    __.log_error("XD: " + str(apartment_id))

    apartment = Apartment.objects.get(id=apartment_id)
    apartment.status = ApartmentStatus.DELETED
    apartment.save()


@celery_task
def fetch_apartments_task(logger: CustomLogger, _, url: str, mails: list[str]):
    from modules.scrapers.services.scraper import ScraperService

    subtasks = ScraperService(logger).fetch_apartments(url, mails)
    return group(subtasks)()


@celery_task
def scraper_master_task(__, _, url: str, mails: list[str]):
    fetch_apartments_task.s(url, mails).delay()


@celery_task
def handle_tasks_done(logger: CustomLogger, _, result, mails: list[str]):
    logger.log_info("All tasks are done!")

    for mail in mails:
        test_mail.delay(mail)
    return result
