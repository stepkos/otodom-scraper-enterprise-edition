#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

# run celery
#celery -A config worker --loglevel=info --concurrency 1 -E
celery -A config worker --loglevel=info

# run celery beat
#celery -A config worker -l info -B --scheduler django_celery_beat.schedulers:DatabaseScheduler
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
