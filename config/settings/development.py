from .base import *

DEBUG = True

# '*' means all hosts are allowed.
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        # The database engine to use.
        "ENGINE": "django.db.backends.sqlite3",
        # The name of the database file.
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Cache configs for development
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Celery
CELERY_BROKER_URL = "amqp://localhost"
CELERY_RESULT_BACKEND = "rpc://"
