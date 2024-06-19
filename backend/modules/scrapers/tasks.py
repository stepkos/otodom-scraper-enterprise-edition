from decimal import Decimal

from celery import group

from modules.apartments.constants import ApartmentStatus
from modules.apartments.models import Apartment, ApartmentDetails
from modules.core.utils import celery_task
from modules.emails.tasks import send_offers
from modules.scrapers.models import ScraperSession
from modules.scrapers.services.custom_logger import CustomLogger
from modules.valuations.ml.predictions import predict_with_scalers_from_apartment


@celery_task
def fetch_apartment_details_task(logger: CustomLogger, _, apartment_id):
    from modules.scrapers.services.scraper import ScraperService

    apartment = Apartment.objects.get(id=apartment_id)
    return ScraperService(logger).fetch_apartment_details(apartment)


@celery_task
def valuate_task(logger, _, ___, apartment_id):
    apartment = Apartment.objects.get(id=apartment_id)
    try:
        if est_price := predict_with_scalers_from_apartment(apartment):

            apartment.estimated_price = Decimal(str(est_price * float(apartment.area)))
            logger.log_info(f"Estimated market price: {est_price}")
            apartment.status = ApartmentStatus.VALUATED
            apartment.save()
        else:
            logger.log_error(f"Could not estimate for this apartment: {apartment_id}, details: {apartment.details.id}")
    except ApartmentDetails.DoesNotExist:
        logger.log_error(f"No deatail for: {apartment_id}, status: {apartment.status}")


@celery_task
def fetch_apartments_task(
        logger: CustomLogger, _, session_id, url: str, mails: list[str]
):
    from modules.scrapers.services.scraper import ScraperService

    subtasks = ScraperService(logger).fetch_apartments(session_id, url, mails)
    return group(subtasks)()


@celery_task
def scraper_master_task(__, _, url: str, mails: list[str], treshold: float, artificial_page_stop: int | None = None):
    session = ScraperSession.objects.create(url=url, treshold=treshold, artificial_page_stop=artificial_page_stop)
    fetch_apartments_task.s(session.id, url, mails).delay()


@celery_task
def handle_tasks_done(logger: CustomLogger, _, session_id, mails: list[str]):
    session = ScraperSession.objects.get(id=session_id)
    logger.log_info(f"All tasks are done! Looking for special offers, treshold {session.treshold}")

    special_offers_ids = []
    for apart in session.apartments.all():
        if apart.is_special_offer(session.treshold):
            logger.log_info("Special offer, below price:" + str(apart.below_market_price))
            special_offers_ids.append(apart.id)
        elif apart.estimated_price is None:
            logger.log_error(f"No est price for: {apart.id}")
        else:
            logger.log_info(f"This is not so special: {apart.price}, market: {apart.estimated_price}")

    logger.log_info(f"Found {len(special_offers_ids)} special offers")

    for mail in mails:
        send_offers.delay(mail, special_offers_ids)
        logger.log_info(f"Sent to {mail}")
