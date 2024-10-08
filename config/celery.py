import os

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

load_dotenv()

# Set the default Django settings module based on the MODE environment variable
mode = os.getenv("MODE", "development")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{mode}")

app = Celery("deal")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

CELERY_BEAT_SCHEDULE = {
    "send-account-activity-reports": {
        "task": "django.core.management.call_command",
        "schedule": crontab(
            hour="0", minute="0", day_of_week="monday"
        ),  # Every Monday at midnight
        "args": ("generate_reports",),
    },
}
