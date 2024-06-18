from celery.utils.log import get_task_logger

from modules.core.utils import celery_task

logger = get_task_logger(__name__)


@celery_task
def hello(self):
    logger.info("Hello world")
    logger.info(self)
    return {"nice": "hello world"}
