from django.core.management.base import BaseCommand

from local_apps.accounts.models import User
from local_apps.accounts.tasks import send_account_activity_report


class Command(BaseCommand):
    help = "Generate account activity reports and send them to users"

    def handle(self, *args, **options):
        users = User.objects.filter(is_active=True, receive_reports=True)

        for user in users:
            send_account_activity_report.delay(user.id)
        self.stdout.write(
            self.style.SUCCESS("Successfully sent account activity reports")
        )
