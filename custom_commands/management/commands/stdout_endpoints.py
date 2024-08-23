from django.core.management.base import BaseCommand
from django.urls import get_resolver


class Command(BaseCommand):
    help = "Displays all URL patterns in the project"

    def handle(self, *args, **kwargs):
        url_patterns = get_resolver().url_patterns
        self.stdout.write("# API Endpoints\n")
        for pattern in url_patterns:
            self.stdout.write(f"## {pattern.name}\n")
            self.stdout.write(f"**Pattern:** `{pattern.pattern}`\n")
            self.stdout.write(
                f"**View:** `{pattern.callback.__module__}.{pattern.callback.__name__}`\n"
            )
            self.stdout.write("\n")
