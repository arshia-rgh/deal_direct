from .base import *

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # The database backend to use.
        "NAME": os.environ.get("DB_NAME"),  # The name of the database.
        "USER": os.environ.get("DB_USER"),  # The username to connect to the database.
        "PASSWORD": os.environ.get(
            "DB_PASSWORD"
        ),  # The password to connect to the database.
        "HOST": os.environ.get("DB_HOST"),  # The host of the database.
        "PORT": os.environ.get("DB_PORT"),  # The port of the database.
    }
}

# Cache configs (use redis in production)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Celery
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "rpc://")
