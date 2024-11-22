# ---- Standard Library Imports ----
import logging

# ---- Third-Party Imports ----
from django.shortcuts import render
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

# ---- Logger Configuration ----
logger = logging.getLogger(__name__)

# ---- Constants ----
PROTECTED_VIEWS = [
    'edit_profile',
    'change_password',
    'profile_view',
]


# ---- Middleware for Logging Protected Page Access ----
class LogProtectedPageAccessMiddleware(MiddlewareMixin):
    """
    Middleware to log attempts to access protected pages.

    Logs a warning if an unauthenticated user tries to access a protected page.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Process the request to log unauthenticated access attempts.

        :param request: The HTTP request object.
        :type request: HttpRequest
        :param view_func: The view function being called.
        :type view_func: function
        :param view_args: Positional arguments passed to the view.
        :type view_args: tuple
        :param view_kwargs: Keyword arguments passed to the view.
        :type view_kwargs: dict
        :return: None
        :rtype: NoneType
        """
        resolver_match = resolve(request.path_info)
        view_name = resolver_match.url_name

        if view_name in PROTECTED_VIEWS:
            if not request.user.is_authenticated:
                logger.warning(
                    f"Unauthenticated access attempt to protected page: "
                    f"{request.path_info} from IP: {request.META.get('REMOTE_ADDR')}"
                )
        return None


# ---- Middleware for Handling Errors ----
class HandleErrorMiddleware(MiddlewareMixin):
    """
    Middleware to handle 404 and 500 errors.

    Provides custom rendering for error pages and logs relevant details.
    """

    def process_response(self, request, response):
        """
        Customize responses for specific HTTP error statuses.

        :param request: The HTTP request object.
        :type request: HttpRequest
        :param response: The HTTP response object.
        :type response: HttpResponse
        :return: Rendered error page or the original response.
        :rtype: HttpResponse
        """
        if response.status_code == 404:
            logger.warning(f"Page not found: {request.path_info}")
            return render(request, 'ums/404.html', status=404)
        elif response.status_code == 500:
            logger.error(f"Server error at {request.path_info}")
            return render(request, 'ums/500.html', status=500)
        return response

    def process_exception(self, request, exception):
        """
        Handle uncaught exceptions by logging and rendering a 500 error page.

        :param request: The HTTP request object.
        :type request: HttpRequest
        :param exception: The exception that occurred.
        :type exception: Exception
        :return: Rendered 500 error page.
        :rtype: HttpResponse
        """
        logger.error(f"Exception occurred: {exception}", exc_info=True)
        return render(request, 'ums/500.html', status=500)
