from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import HttpResponse


class AnonymousUserCacheMiddleware(MiddlewareMixin):
    """
    Middleware to cache responses for anonymous users on specific paths.

    Features:
    - Caches GET requests for anonymous users on pre-defined paths.
    - Retrieves cached responses to reduce server load and response time.
    - Does not affect authenticated users or non-GET requests.

    Attributes:
        PATHS_TO_CACHE (list): Paths eligible for caching.
    """
    PATHS_TO_CACHE = [
        '/books/list/',
    ]

    def process_request(self, request):
        """
        Handle incoming requests and return cached responses if applicable.

        For anonymous users making GET requests to paths in `PATHS_TO_CACHE`,
        attempts to retrieve the cached response.

        :param request: The HTTP request object.
        :return: Cached HttpResponse if available, otherwise None.
        """
        if request.user.is_authenticated:
            return None
        if request.method != 'GET':
            return None
        if request.path not in self.PATHS_TO_CACHE:
            return None

        cache_key = 'anonymous_cache_%s' % request.get_full_path()
        response = cache.get(cache_key)
        if response:
            return HttpResponse(response)

    def process_response(self, request, response):
        """
        Cache the response for eligible requests.

        Stores the response content in the cache for GET requests to paths
        in `PATHS_TO_CACHE` made by anonymous users.

        :param request: The HTTP request object.
        :param response: The HTTP response object.
        :return: The original response, after caching if applicable.
        """
        if request.user.is_authenticated:
            return response
        if request.method != 'GET':
            return response
        if request.path not in self.PATHS_TO_CACHE:
            return response

        cache_key = 'anonymous_cache_%s' % request.get_full_path()
        cache.set(cache_key, response.content, 60 * 15)  # Cache for 15 minutes
        return response
