#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done


celery -A config worker --loglevel=info -E
