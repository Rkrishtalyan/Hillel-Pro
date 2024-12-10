"""
Custom template tags for the web_site app.

This module defines custom filters and tags for use in Django templates.
"""

from django import template
from web_site.models import Article


register = template.Library()


# Task 4

@register.filter
def truncate_charts(value, num=20):
    """
    Truncate a string to a specified number of characters.

    If the length of the string exceeds the specified number, it appends '...'
    to indicate truncation.

    :param value: The string to be truncated.
    :type value: str
    :param num: The maximum number of characters to retain (default is 20).
    :type num: int
    :return: The truncated string with '...' appended if truncation occurred.
    :rtype: str
    """
    if len(value) > num:
        return value[:num] + '...'
    return value


@register.simple_tag
def latest_articles(count=5):
    """
    Retrieve the latest articles from the database.

    Orders articles by their ID in descending order and returns the specified
    number of articles.

    :param count: The number of latest articles to retrieve (default is 5).
    :type count: int
    :return: A queryset of the latest articles.
    :rtype: QuerySet
    """
    return Article.objects.order_by('-id')[:count]
