from decimal import Decimal
from random import random

from celery import group

from modules.apartments.models import Apartment
from modules.core.utils import celery_task
from modules.emails.tasks import send_offers
from modules.scrapers.models import ScraperSession
from modules.scrapers.services.custom_logger import CustomLogger


@celery_task
def fetch_apartment_details_task(logger: CustomLogger, _, apartment_id):
    from modules.scrapers.services.scraper import ScraperService

    apartment = Apartment.objects.get(id=apartment_id)
    return ScraperService(logger).fetch_apartment_details(apartment)


@celery_task
def valuate_task(__, _, ___, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    if apartment.price:
        apartment.estimated_price = apartment.price + apartment.price * Decimal(str(random()))
        apartment.save()


@celery_task
def fetch_apartments_task(logger: CustomLogger, _, session_id, url: str, mails: list[str]):
    from modules.scrapers.services.scraper import ScraperService
    subtasks = ScraperService(logger).fetch_apartments(session_id, url, mails)
    return group(subtasks)()


@celery_task
def scraper_master_task(__, _, url: str, mails: list[str], treshold: float):
    session = ScraperSession.objects.create(url=url, treshold=treshold)
    fetch_apartments_task.s(session.id, url, mails).delay()


@celery_task
def handle_tasks_done(logger: CustomLogger, _, session_id, mails: list[str]):
    logger.log_info("All tasks are done!")
    session = ScraperSession.objects.get(id=session_id)

    special_offers_ids = []
    for apart in session.apartments.all():
        logger.log_info(str(apart.is_special_offer(session.treshold)))
        logger.log_info(str(apart.below_market_price))
        logger.log_info(str(apart.price))
        logger.log_info(str(apart.estimated_price))

        if apart.is_special_offer(session.treshold):
            special_offers_ids.append(apart.id)

    for mail in mails:
        send_offers.delay(mail, special_offers_ids)
