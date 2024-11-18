from django_filters import rest_framework as filters
from .models import Book

class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    genre = filters.CharFilter(field_name="genre", lookup_expr="icontains")
    author = filters.CharFilter(field_name="author", lookup_expr="icontains")
    publication_year_after = filters.NumberFilter(field_name="publication_year", lookup_expr="gte")
    publication_year_before = filters.NumberFilter(field_name="publication_year", lookup_expr="lte")

    class Meta:
        model = Book
        fields = ['title', 'genre', 'author', 'publication_year']
