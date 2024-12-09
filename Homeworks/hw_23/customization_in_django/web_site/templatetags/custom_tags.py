from django import template
from web_site.models import Article


register = template.Library()


#Task 4

@register.filter
def truncate_charts(value, num=20):
    if len(value) > num:
        return value[:num] + '...'
    return value


@register.simple_tag
def latest_articles(count=5):
    return Article.objects.order_by('-id')[:count]
