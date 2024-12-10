"""
Utility functions for the web_site app.

This module provides helper functions for specific operations related to
the web_site application.
"""

from web_site.models import Article


# Task 8

def fetch_reviewed_news_articles():
    """
    Fetch reviewed articles in the 'news' category.

    Executes a raw SQL query to retrieve all articles where:
    - The category is 'news'.
    - The reviewed status is True.

    :return: A queryset of reviewed news articles.
    :rtype: RawQuerySet
    """
    return Article.objects.raw(
        "SELECT * FROM web_site_article WHERE category = %s AND reviewed = %s",
        ['news', True]
    )
