"""
Define custom permissions for the application.

This module includes the `IsAuthorOrReadOnly` permission class, which enforces that
users can only modify objects if they are the author, while allowing read-only access
for all users.

Classes:
    - IsAuthorOrReadOnly: Custom permission to restrict write access to authors.

Dependencies:
    - Django REST framework's permissions.
"""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access to all users and write access only to the author of an object.

    Methods:
        - has_object_permission: Determine if the request has the required permissions
          based on the user's role and the object's author.

    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform actions on the object.

        Read-only permissions are allowed for any request (SAFE_METHODS).
        Write permissions are only allowed if the user is the author of the object.

        :param request: The current request instance.
        :type request: HttpRequest
        :param view: The view the permission check is being applied to.
        :type view: View
        :param obj: The object being accessed.
        :type obj: Any
        :return: True if the permission is granted, False otherwise.
        :rtype: bool
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
