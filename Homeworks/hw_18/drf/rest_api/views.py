"""
Define views for the application.

This module contains views to handle API requests for the `Book` model and user registration.
It utilizes Django REST framework's viewsets and generic views to streamline CRUD operations
and manage permissions.

Classes:
    - BookViewSet: Handles CRUD operations for books, with support for filtering, searching, and ordering.
    - UserRegisterView: Handles user registration via a `CreateAPIView`.

Dependencies:
    - Django REST framework's generics, permissions, and viewsets.
    - Django Filters for query filtering.
    - REST framework's pagination for paginated responses.
    - Django's `User` model for managing user accounts.
    - Application-specific models, serializers, filters, and pagination classes.
"""
from rest_framework import generics, permissions, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer, UserRegisterSerializer
from .filters import BookFilter
from .pagination import BookPagination


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing books.

    This class provides CRUD operations for the `Book` model, including features such as filtering,
    searching, ordering, and paginated responses. Permissions are adjusted dynamically based on
    the action being performed.

    Attributes:
        - queryset: Queryset for retrieving all book objects.
        - serializer_class: Serializer class used for serializing and deserializing book objects.
        - filter_backends: Filters applied for querying the book list.
        - filterset_class: Custom filter class for advanced querying.
        - search_fields: Fields available for search functionality.
        - ordering_fields: Fields available for ordering results.
        - pagination_class: Custom pagination class for paginated responses.
        - permission_classes: Default permissions applied to all actions.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = BookFilter
    search_fields = ['title']
    ordering_fields = ['title', 'publication_year']
    pagination_class = BookPagination
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the user as the owner of the book during creation.

        :param serializer: The serializer instance containing validated data.
        :type serializer: BookSerializer
        """
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """
        Dynamically set permissions based on the action.

        - Admin permission is required for the 'destroy' action.
        - Authenticated users can access all other actions.

        :return: The appropriate list of permission classes.
        :rtype: list
        """
        if self.action == 'destroy':
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super(BookViewSet, self).get_permissions()


class UserRegisterView(generics.CreateAPIView):
    """
    View for user registration.

    This view allows users to register by providing the necessary information.
    It uses a serializer to validate and create the user account.

    Attributes:
        - queryset: Queryset for the `User` model.
        - serializer_class: Serializer class used for handling user registration.
        - permission_classes: Allow all users to access this endpoint.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
