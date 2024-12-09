from django import forms
from django.core.exceptions import ValidationError


# Task 2

def validate_body_contains_curse_words(value):
    if "fuck" in value.lower():
        raise ValidationError("Watch your language!.")


class CustomSelectWidget(forms.Select):
    template_name = 'widgets/custom_select.html'

    def __init__(self, attrs=None, choices=()):
        default_attrs = {'class': 'custom-select-widget', 'label': 'Category'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, choices=choices)


class ArticleForm(forms.Form):
    title = forms.CharField(max_length=255, label="Title")
    body = forms.CharField(
        widget=forms.Textarea,
        validators=[validate_body_contains_curse_words],
        label="Body (avoid using mature words)"
    )
    category = forms.ChoiceField(
        choices=[
            ('tech', 'Technology'),
            ('lifestyle', 'Lifestyle'),
            ('news', 'News')
        ],
        widget=CustomSelectWidget,
        label="Category"
    )
