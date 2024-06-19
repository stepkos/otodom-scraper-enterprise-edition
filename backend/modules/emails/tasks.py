from celery import shared_task
from celery.utils.log import get_task_logger

from modules.apartments.models import Apartment
from modules.emails.services import EmailService

logger = get_task_logger(__name__)


@shared_task
def send_offers(receiver: str, offers: list[Apartment]) -> bool:
    logger.info("Sending email to receiver")
    is_success = EmailService().send_offers(receiver, offers)
    logger.info(f"Email success: {is_success}")
    return is_success


@shared_task
def test_mail(receiver: str) -> bool:
    offers = list(Apartment.objects.all()[:5])
    is_success = EmailService().send_offers(receiver, offers)
    return is_success
