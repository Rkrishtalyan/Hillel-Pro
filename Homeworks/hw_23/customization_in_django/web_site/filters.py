"""
Filters for the web_site app.

This module defines custom filters for querying models in the web_site app.
"""

import django_filters

from web_site.models import Article


# Task 7

class ArticleFilter(django_filters.FilterSet):
    """
    Filter for the Article model.

    Allows filtering articles by their category using an exact match.

    :var category: Filter for the category field with an exact match lookup.
    :type category: django_filters.CharFilter
    """

    category = django_filters.CharFilter(field_name='category', lookup_expr='exact')

    class Meta:
        """
        Meta options for the ArticleFilter class.

        Specifies the model and fields available for filtering.
        """
        model = Article
        fields = ['category']
