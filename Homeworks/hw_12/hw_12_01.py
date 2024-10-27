"""
Завдання 1. Перевірка валідності email.

Напишіть функцію, яка перевіряє, чи є email-адреса валідною. Email вважається валідним,
якщо він має формат example@domain.com, де:

example — послідовність з букв, цифр або точок (але точка не може бути на початку або в кінці).
domain — послідовність з букв або цифр.
.com, .net, .org тощо — домен верхнього рівня (TLD) довжиною від 2 до 6 символів.
"""

import re


def validate_email(email):
    """
    Validate the provided email format.

    This function checks if the email matches a specific regex pattern, ensuring it follows a
    general email structure with alphanumeric characters, optional dots, and a domain.

    :param email: The email address to validate.
    :type email: str
    :return: True if email format is valid, otherwise False.
    :rtype: bool
    """
    # ---- Validate email format ----
    if re.fullmatch(r'\w[\w\.]+\w@\w+\.\w{2,6}', email):
        return True
    return False


# ---- Test email validation function ----
print(validate_email('example@domain.com'))
