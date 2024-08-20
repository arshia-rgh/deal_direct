from .base import *

# Debug mode. When set to True, Django will display a detailed error page whenever an exception is raised.
DEBUG = True

# List of allowed hosts for this site.
# '*' means all hosts are allowed.
ALLOWED_HOSTS = ["*"]

# Database configuration.
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        # The database engine to use.
        "ENGINE": "django.db.backends.sqlite3",
        # The name of the database file.
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
