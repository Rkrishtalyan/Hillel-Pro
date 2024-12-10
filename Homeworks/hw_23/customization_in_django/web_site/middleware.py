import logging
from django.db import transaction
from web_site.models import SiteMetric


# Task 5

class CustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Custom-Header'] = 'MyCustomValue'
        return response


# Task 9

logger = logging.getLogger('web_site.custom')

class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        with transaction.atomic():
            metric, created = SiteMetric.objects.get_or_create(id=1)
            metric.request_count = metric.request_count + 1
            metric.save(update_fields=['request_count'])

        logger.info(f"Request #{metric.request_count} received: {request.path}")

        return response
