from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.core.cache import cache

class RequestCounterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request_count = cache.get('request_count', 0)
        cache.set('request_count', request_count + 1)

