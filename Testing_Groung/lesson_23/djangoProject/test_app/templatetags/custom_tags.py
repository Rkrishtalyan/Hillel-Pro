from django import template
from datetime import datetime


register = template.Library()

@register.filter
def word_count(value):
    return len(value.split())

@register.simple_tag
def greet_user(value):
    return f"Hello {value}"


@register.simple_tag
def current_date():
    return datetime.now()