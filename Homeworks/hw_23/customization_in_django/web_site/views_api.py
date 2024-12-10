"""
API views for the web_site app.

This module defines class-based API views for handling CRUD operations
on articles using Django REST Framework.
"""

from rest_framework import generics

from web_site.models import Article
from web_site.serializers import ArticleSerializer
from web_site.permissions import IsAuthenticatedOrReadOnly
from web_site.filters import ArticleFilter


# Task 7

class ArticleListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating articles.

    - Allows authenticated users to create articles.
    - Provides a list of all articles for any user (read-only access for unauthenticated users).
    - Supports filtering using the ArticleFilter class.

    :var queryset: The queryset of articles to be retrieved or created.
    :var serializer_class: The serializer class used for validating and serializing articles.
    :var permissions_classes: Permissions required to access the view.
    :var filterset_class: The filter class for filtering articles.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permissions_classes = (IsAuthenticatedOrReadOnly,)
    filterset_class = ArticleFilter


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, or deleting a single article.

    - Allows authenticated users to update or delete an article.
    - Provides read-only access to a single article for unauthenticated users.

    :var queryset: The queryset of articles to be retrieved, updated, or deleted.
    :var serializer_class: The serializer class used for validating and serializing articles.
    :var permissions_classes: Permissions required to access the view.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permissions_classes = (IsAuthenticatedOrReadOnly,)
