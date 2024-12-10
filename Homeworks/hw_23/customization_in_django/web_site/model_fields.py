import re
from django.db import models
from django.core.exceptions import ValidationError


# Task 10

PHONE_NUMBER_REGEX = re.compile(r'^\+\d{10,12}$')


def validate_phone_number(value):
    if not PHONE_NUMBER_REGEX.match(value):
        raise ValidationError("Phone number must start with '+' and contain 10 to 12 digits.")


class PhoneNumberField(models.CharField):
    description = "A phone number field that requires a + sign and 10-12 digits."

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 13)
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        if value is None:
            return value
        return value.strip()

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        validate_phone_number(value)
