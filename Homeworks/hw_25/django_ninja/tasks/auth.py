from ninja.security import HttpBearer
from typing import Optional
from django.contrib.auth.models import User
from ninja.errors import HttpError

from tasks.models import Token


class AuthBearer(HttpBearer):
    """
    Provide token-based authentication using the HttpBearer scheme.

    AuthBearer validates the token provided in the request headers and
    retrieves the associated user if the token is valid.

    :raises HttpError: If the token is invalid or missing.
    """

    def authenticate(self, request, token: str) -> Optional[User]:
        """
        Authenticate a user using a token.

        :param request: The incoming request object.
        :type request: HttpRequest
        :param token: The token string extracted from the authorization header.
        :type token: str
        :return: The authenticated user instance or None if authentication fails.
        :rtype: Optional[User]

        :raises HttpError: If the token does not exist or is invalid.
        """
        try:
            token_obj = Token.objects.get(key=token)
            return token_obj.user
        except Token.DoesNotExist:
            raise HttpError(401, "Invalid or missing token.")
