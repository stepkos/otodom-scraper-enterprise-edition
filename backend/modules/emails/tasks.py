from modules.apartments.models import Apartment
from modules.core.utils import celery_task
from modules.emails.services import EmailService


@celery_task
def send_offers(logger, _, receiver: str, offers: list[Apartment]) -> bool:
    logger.log_info("Sending email to receiver")
    is_success = EmailService().send_offers(receiver, offers)
    logger.log_info(f"Email success: {is_success}")
    return is_success


@celery_task
def test_mail(__, _, receiver: str) -> bool:
    offers = list(Apartment.objects.all()[:5])
    is_success = EmailService().send_offers(receiver, offers)
    return is_success
