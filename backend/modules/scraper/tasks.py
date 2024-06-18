from celery.utils.log import get_task_logger

from modules.apartments.models import Apartment
from modules.core.utils import celery_task

logger = get_task_logger(__name__)


@celery_task
def hello(self):
    logger.info("Hello world")
    logger.info(self)
    return {"nice": "hello world"}


@celery_task
def fetch_apartment_details(self, apartment: Apartment):
    # create details or update if exists
    ...


@celery_task
def follow_apartments_by_url(self, url: str):
    # lece po listview
    # dodaje taski sprawdzania details
    ...
