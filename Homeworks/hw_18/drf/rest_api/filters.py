"""
Define filters for the application's models.

This module provides filtering capabilities for the `Book` model using Django Filters.
The `BookFilter` class allows filtering books based on title, genre, author, and
publication year with options for range-based filtering.

Classes:
    - BookFilter: Provides filters for querying the `Book` model.

Dependencies:
    - Django Filters for REST framework.
    - `Book` model.
"""
from django_filters import rest_framework as filters
from .models import Book


class BookFilter(filters.FilterSet):
    """
    Filter books based on various attributes.

    This class defines filters for querying `Book` instances by their title, genre, author,
    and publication year with range-based filters for years.

    Fields:
        - title: Case-insensitive substring matching for book title.
        - genre: Case-insensitive substring matching for book genre.
        - author: Case-insensitive substring matching for author name.
        - publication_year_after: Filter books published in or after a specific year.
        - publication_year_before: Filter books published in or before a specific year.
    """
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    genre = filters.CharFilter(field_name="genre", lookup_expr="icontains")
    author = filters.CharFilter(field_name="author", lookup_expr="icontains")
    publication_year_after = filters.NumberFilter(field_name="publication_year", lookup_expr="gte")
    publication_year_before = filters.NumberFilter(field_name="publication_year", lookup_expr="lte")

    class Meta:
        """
        Meta options for the `BookFilter`.

        Attributes:
            model: The model for which the filter is applied.
            fields: The list of fields that can be filtered.
        """
        model = Book
        fields = ['title', 'genre', 'author', 'publication_year']
