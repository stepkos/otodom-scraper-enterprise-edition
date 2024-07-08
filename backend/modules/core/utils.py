import itertools
import json
from functools import wraps

from celery import chain

from config import celery_app
from modules.core.models import CeleryResult
from modules.scrapers.services.custom_logger import CustomLogger, celery_logger


def celery_task(func):
    @celery_app.task(bind=True, ignore_result=False)
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = CustomLogger(celery_logger)

        task_id = kwargs.get("task_id", None) or args[0].request.id
        task_name = kwargs.get("task_name", None) or args[0].name
        result = func(logger, *args, **kwargs)

        logger_res = logger.get_result_dict()
        is_success = logger_res.pop("success", False)
        logs = logger_res.pop("logs", False)
        errors = logger_res.pop("errors", False)

        CeleryResult.objects.create(
            task_id=task_id,
            task_name=task_name,
            arguments=[list(map(str, args[1::])), kwargs],
            result=(
                result
                if is_json_serializable(result) and not isinstance(result, chain)
                else None
            ),
            is_success=is_success,
            logs=logs,
            errors=errors,
        )
        return result

    return wrapper


def is_json_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except TypeError:
        return False


def flatten(nested_list):
    if isinstance(nested_list, list):
        return list(itertools.chain.from_iterable(map(flatten, nested_list)))
    else:
        return [nested_list]
