"""
Custom permissions for the web_site app.

This module defines custom permissions for API views using Django REST Framework.
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


# Task 7

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission to allow authenticated users to perform any request,
    while unauthenticated users are limited to safe (read-only) methods.
    """

    def has_permission(self, request, view):
        """
        Determine if the user has permission to access the view.

        - Allows read-only access (GET, HEAD, OPTIONS) for all users.
        - Requires authentication for other methods (POST, PUT, DELETE, etc.).

        :param request: The HTTP request object.
        :type request: HttpRequest
        :param view: The view being accessed.
        :type view: View
        :return: True if the user has permission, False otherwise.
        :rtype: bool
        """
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated
