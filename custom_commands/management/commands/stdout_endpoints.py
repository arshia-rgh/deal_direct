from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern, URLResolver
from django.conf import settings


class Command(BaseCommand):
    help = "Displays all URL patterns in the project"

    def handle(self, *args, **kwargs):
        url_patterns = get_resolver().url_patterns
        self.stdout.write("# API Endpoints\n")
        self._print_patterns(url_patterns)

    def _print_patterns(self, patterns, prefix=""):
        local_apps = [
            app.split(".")[0]
            for app in settings.INSTALLED_APPS
            if not app.startswith("django.")
        ]
        for pattern in patterns:
            if isinstance(pattern, URLPattern):
                view_module = pattern.callback.__module__.split(".")[0]
                if view_module in local_apps:
                    self.stdout.write(f"## {pattern.name or 'Unnamed'}\n")
                    self.stdout.write(f"**Pattern:** `{prefix}{pattern.pattern}`\n")
                    self.stdout.write(
                        f"**View:** `{pattern.callback.__module__}.{pattern.callback.__name__}`\n"
                    )
                    self.stdout.write("\n")
            elif isinstance(pattern, URLResolver):
                self._print_patterns(
                    pattern.url_patterns, prefix + str(pattern.pattern)
                )
