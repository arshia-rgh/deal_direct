import logging

from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle


class ListCacheMixin:
    """
    Mixin to cache the list of queryset results.

    Attributes:
        cache_key (str): The key to use for caching the queryset.
        timeout (int): The cache timeout in seconds. Default is 15 minutes.

    Methods:
        list(request, *args, **kwargs): Retrieves the list of queryset results from the cache if available,
                                        otherwise fetches from the database and caches the results.
    """

    cache_key = None
    timeout = 60 * 15

    def list(self, request, *args, **kwargs):
        if not self.cache_key:
            raise ValueError("cache_key can not be None")

        cached_queryset = cache.get(self.cache_key)

        if not cached_queryset:
            cached_queryset = list(self.queryset)
            cache.set(self.cache_key, cached_queryset, self.timeout)

        serializer = self.get_serializer(cached_queryset, many=True)
        return Response(serializer.data)


class ThrottleMixin:
    """
    Mixin to apply scoped rate throttling to viewsets.

    Methods:
        get_throttles(): Determines the throttle scope based on the request method and returns a list of throttles.
    """

    def get_throttles(self):
        if self.request.method in ["PATCH", "PUT", "POST"]:
            self.throttle_scope = "uploads"

        else:
            self.throttle_scope = "receives"
        return [ScopedRateThrottle()]


class LoggingMixin:
    logger = logging.getLogger(__name__)

    def dispatch(self, request, *args, **kwargs):
        user = request.user if request.user.is_autenticated else "Anonymous"
        self.logger.info(
            f"User: {user}, Request: {request.method} {request.get_full_path()}"
        )

        response = super().dispatch(request, *args, **kwargs)

        self.logger.info(
            f"User: {user}, Response: {response.status_code} {response.data}"
        )

        return response
