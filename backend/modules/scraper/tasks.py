from celery.utils.log import get_task_logger
from celery import shared_task

logger = get_task_logger(__name__)


@shared_task
def hello():
    logger.info("Hello world")
    return "hello world"


