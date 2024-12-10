from django import forms
from django.core.exceptions import ValidationError
import re


# Task 10

PHONE_NUMBER_REGEX = re.compile(r'^\+\d{10,12}$')

class PhoneNumberFormField(forms.CharField):
    def validate(self, value):
        super().validate(value)
        if not PHONE_NUMBER_REGEX.match(value):
            raise ValidationError("Phone number must start with '+' and contain 10 to 12 digits.")
