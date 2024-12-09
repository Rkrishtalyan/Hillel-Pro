from rest_framework.permissions import BasePermission, SAFE_METHODS


# Task 7

class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated
