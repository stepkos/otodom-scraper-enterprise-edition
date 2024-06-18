#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

celery -A config worker -l info -B --scheduler django_celery_beat.schedulers:DatabaseScheduler
