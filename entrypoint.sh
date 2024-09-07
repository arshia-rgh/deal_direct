#!/bin/sh
# Run database migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL || true

# Start the ASGI server
uvicorn  config.asgi:application --host 0.0.0.0 --port 8000
