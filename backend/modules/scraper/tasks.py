from celery import shared_task
from celery.utils.log import get_task_logger

from config.celery import app

logger = get_task_logger(__name__)


@app.task(bind=True, ignore_result=False)
def hello(self):
    logger.info("Hello world")
    logger.info(self)
    return {"nice": "hello world"}
