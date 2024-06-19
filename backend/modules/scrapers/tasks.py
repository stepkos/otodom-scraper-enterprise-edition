from itertools import chain
from random import random

from celery import chord, group

from modules.apartments.models import Apartment
from modules.core.utils import celery_task, flatten
from modules.emails.tasks import test_mail
from modules.scrapers.services.custom_logger import CustomLogger


@celery_task
def fetch_apartment_details_task(logger: CustomLogger, _, apartment_id, mails: list[str]):
    from modules.scrapers.services.scraper import ScraperService

    apartment = Apartment.objects.get(id=apartment_id)
    return ScraperService(logger, mails).fetch_apartment_details(apartment)


@celery_task
def valuate_task(__, _, apartment_id, mails: list[str]):
    apartment = Apartment.objects.get(id=apartment_id)
    apartment.price = random() * 1000
    apartment.save()


@celery_task
def fetch_apartments_task(logger: CustomLogger, _, url: str, mails: list[str]):
    from modules.scrapers.services.scraper import ScraperService

    subtasks = ScraperService(logger, mails).fetch_apartments(url)
    return group(subtasks)()


@celery_task
def scraper_master_task(__, _, url: str, mails: list[str]):
    fetch_apartments_task.s(url, mails).delay()


@celery_task
def handle_tasks_done(logger: CustomLogger, _, result, mails: list[str]):
    logger.log_info("result")
    logger.log_info("All tasks are done!")

    logger.log_info(str(list(filter(lambda x: x is not None, flatten(result)))))

    for mail in mails:
        test_mail.delay(mail)
    return result
