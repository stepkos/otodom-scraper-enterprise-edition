from celery.utils.log import get_task_logger
from celery import shared_task

from modules.apartments.models import Apartment, ApartmentDetails
from modules.emails.services import EmailService

logger = get_task_logger(__name__)


@shared_task
def send_offers(receiver: str, offers: list[tuple[Apartment, ApartmentDetails]]) -> bool:
    logger.info("Sending email to receiver")
    is_success = EmailService().send_offers(receiver, offers)
    logger.info(f"Email success: {is_success}")
    return is_success


@shared_task
def test_mail(receiver: str) -> bool:
    aps = list(Apartment.objects.all()[:5])
    aps_details = list(ap.details for ap in aps)
    offers = list(zip(aps, aps_details))
    logger.info("Sending email to receiver")
    is_success = EmailService().send_offers(receiver, offers)
    logger.info(f"Email success: {is_success}")
    return is_success


