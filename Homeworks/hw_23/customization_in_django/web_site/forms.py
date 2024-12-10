"""
Forms for the web_site app.

This module defines custom forms and form fields for the web_site application.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
import re

from web_site.models import CustomUser, Contact
from web_site.form_fields import PhoneNumberFormField


# Task 2

def validate_body_contains_curse_words(value):
    """
    Validate that the body field does not contain prohibited words.

    Raises a ValidationError if any curse words are detected.

    :param value: The text to validate.
    :type value: str
    :raises ValidationError: If the text contains curse words.
    """
    if "fuck" in value.lower():
        raise ValidationError("Watch your language!.")


class CustomSelectWidget(forms.Select):
    """
    Custom widget for rendering select fields with additional styling and labels.

    Uses a template and default attributes for consistent appearance.
    """
    template_name = 'web_site/widgets/custom_select.html'

    def __init__(self, attrs=None, choices=()):
        """
        Initialize the custom select widget with default attributes.

        :param attrs: Optional HTML attributes for the widget.
        :type attrs: dict
        :param choices: The choices for the select field.
        :type choices: tuple
        """
        default_attrs = {'class': 'custom-select-widget', 'label': 'Category'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, choices=choices)


class ArticleForm(forms.Form):
    """
    Form for creating or editing articles.

    Includes fields for title, body, category, and optional contact selection.
    """
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
    """
    Validate that a phone number starts with '+' and contains 10 to 12 digits.

    Uses a regular expression to check the phone number format.

    :param value: The phone number string to validate.
    :type value: str
    :raises ValidationError: If the phone number format is invalid.
    """
    pattern = r'^\+\d{10,12}$'
    if not re.match(pattern, value):
        raise ValidationError("Phone number must start with '+' and contain 10 to 12 digits.")


class RegistrationForm(UserCreationForm):
    """
    Form for user registration with phone number validation.

    Extends Django's UserCreationForm with an additional phone number field.
    """
    phone_number = forms.CharField(
        max_length=13,
        required=True,
        validators=[validate_phone_number],
        label="Phone Number"
    )

    class Meta:
        """
        Meta options for the RegistrationForm class.

        Specifies the model and fields included in the form.
        """
        model = CustomUser
        fields = ['username', 'phone_number', 'password1', 'password2']


# Task 10

class ContactForm(forms.ModelForm):
    """
    Form for creating or editing contact information.

    Includes custom validation for the phone number field.
    """
    phone = PhoneNumberFormField(label="Phone Number")

    class Meta:
        """
        Meta options for the ContactForm class.

        Specifies the model and fields included in the form.
        """
        model = Contact
        fields = ['name', 'phone']
