from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
import re

from web_site.models import CustomUser, Contact
from web_site.form_fields import PhoneNumberFormField


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
    contact = forms.ModelChoiceField(
        queryset=Contact.objects.all(),
        label="Contact",
        required=False
    )


# Task 6

def validate_phone_number(value):
    pattern = r'^\+\d{10,12}$'
    if not re.match(pattern, value):
        raise ValidationError("Phone number must start with '+' and contain 10 to 12 digits.")


class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=13,
        required=True,
        validators=[validate_phone_number],
        label="Phone Number"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'password1', 'password2']


# Task 10

class ContactForm(forms.ModelForm):
    phone = PhoneNumberFormField(label="Phone Number")

    class Meta:
        model = Contact
        fields = ['name', 'phone']
