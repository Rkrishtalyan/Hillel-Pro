import django_filters
from web_site.models import Article


# Task 7

class ArticleFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category', lookup_expr='exact')

    class Meta:
        model = Article
        fields = ['category']
