"""
Custom model fields for the web_site app.

This module defines custom model fields with additional validation for specific use cases.
"""

import re
from django.db import models
from django.core.exceptions import ValidationError


# Task 10

PHONE_NUMBER_REGEX = re.compile(r'^\+\d{10,12}$')


def validate_phone_number(value):
    """
    Validate that a phone number starts with '+' and contains 10 to 12 digits.

    Uses a regular expression to ensure the phone number meets the required format.

    :param value: The phone number string to validate.
    :type value: str
    :raises ValidationError: If the phone number format is invalid.
    """
    if not PHONE_NUMBER_REGEX.match(value):
        raise ValidationError("Phone number must start with '+' and contain 10 to 12 digits.")


class PhoneNumberField(models.CharField):
    """
    A custom model field for storing phone numbers.

    Ensures that the phone number:
    - Starts with a '+'.
    - Contains 10 to 12 digits.
    - Does not exceed 13 characters in length.
    """
    description = "A phone number field that requires a + sign and 10-12 digits."

    def __init__(self, *args, **kwargs):
        """
        Initialize the PhoneNumberField with a default max_length of 13.

        :param args: Positional arguments for the parent class.
        :param kwargs: Keyword arguments for the parent class.
        """
        kwargs.setdefault('max_length', 13)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        """
        Convert the input value to a Python string.

        Strips leading and trailing whitespace from the value if it is not None.

        :param value: The input value to process.
        :type value: str
        :return: The processed phone number string.
        :rtype: str
        """
        value = super().to_python(value)
        if value is None:
            return value
        return value.strip()

    def validate(self, value, model_instance):
        """
        Validate the phone number field value.

        Ensures that the phone number conforms to the required format using
        the validate_phone_number function.

        :param value: The phone number string to validate.
        :type value: str
        :param model_instance: The instance of the model containing this field.
        :type model_instance: Model
        :raises ValidationError: If the phone number format is invalid.
        """
        super().validate(value, model_instance)
        validate_phone_number(value)
