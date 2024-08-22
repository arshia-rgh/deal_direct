from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle


class ListCacheMixin:
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
    def get_throttles(self):
        if self.request.method in ["PATCH", "PUT", "POST"]:
            self.throttle_scope = "uploads"

        else:
            self.throttle_scope = "receives"
        return [ScopedRateThrottle()]
