"""
Middleware for the web_site app.

This module includes custom middleware for adding headers and tracking site metrics.
"""

import logging
from django.db import transaction

from web_site.models import SiteMetric


# Task 5

class CustomHeaderMiddleware:
    """
    Middleware to add a custom header to all responses.

    Adds the 'X-Custom-Header' with a static value to every HTTP response.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.

        :param get_response: The next middleware or view in the request/response chain.
        :type get_response: callable
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the incoming request and add a custom header to the response.

        :param request: The HTTP request object.
        :type request: HttpRequest
        :return: The HTTP response object with the custom header added.
        :rtype: HttpResponse
        """
        response = self.get_response(request)
        response['X-Custom-Header'] = 'MyCustomValue'
        return response


# Task 9

logger = logging.getLogger('web_site.custom')

class MetricsMiddleware:
    """
    Middleware to track and log site metrics.

    Tracks the number of HTTP requests received by incrementing a counter in the SiteMetric model.
    Logs the request count and the requested path.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.

        :param get_response: The next middleware or view in the request/response chain.
        :type get_response: callable
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the incoming request and update site metrics.

        Increments the request count in the SiteMetric model within an atomic transaction
        and logs the request count and path.

        :param request: The HTTP request object.
        :type request: HttpRequest
        :return: The HTTP response object.
        :rtype: HttpResponse
        """
        response = self.get_response(request)

        with transaction.atomic():
            metric, created = SiteMetric.objects.get_or_create(id=1)
            metric.request_count = metric.request_count + 1
            metric.save(update_fields=['request_count'])

        logger.info(f"Request #{metric.request_count} received: {request.path}")

        return response
