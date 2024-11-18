"""
Define custom pagination classes for the application.

This module contains the `BookPagination` class, which customizes pagination behavior
for the `Book` model's API views using page number-based pagination.

Classes:
    - BookPagination: Implements pagination with configurable page size.

Dependencies:
    - Django REST framework's `PageNumberPagination`.
"""
from rest_framework.pagination import PageNumberPagination


class BookPagination(PageNumberPagination):
    """
    Provide pagination for the Book API.

    This class allows paginated responses with a default page size of 10.
    Users can customize the page size and select specific pages using query parameters.

    Attributes:
        - page_size: The default number of items per page.
        - page_size_query_param: The query parameter for clients to override the page size.
        - page_query_param: The query parameter for clients to specify the page number.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
