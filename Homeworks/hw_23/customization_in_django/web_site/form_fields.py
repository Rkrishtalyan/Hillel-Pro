"""
Custom form fields for the web_site app.

This module defines custom form fields to extend Django's default form behavior.
"""

from django import forms
from django.core.exceptions import ValidationError
import re


# Task 10

PHONE_NUMBER_REGEX = re.compile(r'^\+\d{10,12}$')


class PhoneNumberFormField(forms.CharField):
    """
    Custom form field for validating phone numbers.

    Ensures that phone numbers:
    - Start with a '+'.
    - Contain 10 to 12 digits.

    :raises ValidationError: If the phone number does not match the required pattern.
    """

    def validate(self, value):
        """
        Validate the phone number field value.

        Checks if the input matches the PHONE_NUMBER_REGEX pattern. Raises a
        ValidationError if the validation fails.

        :param value: The phone number string to validate.
        :type value: str
        :raises ValidationError: If the phone number format is invalid.
        """
        super().validate(value)
        if not PHONE_NUMBER_REGEX.match(value):
            raise ValidationError(
                "Phone number must start with '+' and contain 10 to 12 digits."
            )
