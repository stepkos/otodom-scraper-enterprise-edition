from functools import wraps

from config.celery import app
from modules.core.models import CeleryResult


def celery_task(func):
    @app.task(bind=True, ignore_result=False)
    @wraps(func)
    def wrapper(*args, **kwargs):
        task_id = kwargs.get('task_id', None) or args[0].request.id
        task_name = kwargs.get('task_name', None) or args[0].name
        result = func(*args, **kwargs)
        CeleryResult.objects.create(task_id=task_id, result=result, task_name=task_name)
        return result

    return wrapper
