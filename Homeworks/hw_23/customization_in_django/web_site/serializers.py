"""
Serializers for the web_site app.

This module defines serializers for converting model instances to JSON
representations and vice versa.
"""

from rest_framework import serializers
from web_site.models import Article, Comment


# Task 7

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.

    Converts Comment instances to and from JSON format, including the
    following fields:
    - id: The unique identifier of the comment.
    - text: The text content of the comment.
    - created_at: The timestamp when the comment was created.
    """

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Article model.

    Converts Article instances to and from JSON format, including the
    following fields:
    - id: The unique identifier of the article.
    - title: The title of the article.
    - body: The body content of the article.
    - category: The category of the article.
    - reviewed: A boolean indicating if the article has been reviewed.
    - comments: Nested serializer for related comments (read-only).
    """
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'body', 'category', 'reviewed', 'comments']
