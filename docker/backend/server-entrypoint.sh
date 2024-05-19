#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done


until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done


# python manage.py createsuperuser --noinput

# for prod
#python manage.py collectstatic --noinput
#gunicorn backend.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4

# for debug
python manage.py runserver 0.0.0.0:8000