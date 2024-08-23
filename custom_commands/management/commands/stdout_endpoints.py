from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern, URLResolver


class Command(BaseCommand):
    help = "Displays all URL patterns in the project"

    def handle(self, *args, **kwargs):
        url_patterns = get_resolver().url_patterns
        self.stdout.write("# API Endpoints\n")
        self._print_patterns(url_patterns)

    def _print_patterns(self, patterns, prefix=""):
        for pattern in patterns:
            if isinstance(pattern, URLPattern):
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
