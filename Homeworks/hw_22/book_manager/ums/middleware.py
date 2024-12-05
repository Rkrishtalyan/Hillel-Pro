from django.utils import timezone
from datetime import timedelta


# ---- Middleware to Auto-Renew Cookies ----
class AutoRenewCookieMiddleware:
    """
    Middleware to auto-renew the 'name' cookie with an extended expiration time.

    This middleware checks for the presence of the 'name' cookie in the request.
    If it exists, it renews the cookie by resetting its expiration time to 30 minutes
    from the current time.

    Attributes:
        get_response (callable): The next middleware or view to handle the request.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.

        :param get_response: The next middleware or view to handle the request.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request and auto-renew the 'name' cookie if it exists.

        :param request: The HTTP request object.
        :return: The HTTP response object with a potentially renewed 'name' cookie.
        """
        response = self.get_response(request)
        if 'name' in request.COOKIES:
            name = request.COOKIES['name']
            expires = timezone.now() + timedelta(minutes=30)
            response.set_cookie('name', name, expires=expires)
        return response
