from ninja.security import HttpBearer
from typing import Optional
from django.contrib.auth.models import User
from ninja.errors import HttpError

from tasks.models import Token


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> Optional[User]:
        try:
            token_obj = Token.objects.get(key=token)
            return token_obj.user
        except Token.DoesNotExist:
            raise HttpError(401, "Invalid or missing token.")
