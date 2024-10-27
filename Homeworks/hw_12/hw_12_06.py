"""
Завдання 6. Перевірка валідності пароля.

Напишіть функцію, яка перевіряє, чи є пароль надійним. Пароль вважається надійним, якщо він:

-   містить як мінімум 8 символів,
-   містить принаймні одну цифру,
-   має хоча б одну велику літеру та одну малу,
-   містить хоча б один спеціальний символ (@, #, $, %, &, тощо).
"""

import re


def validate_password(password):
    """
    Validate the strength of a password based on specific criteria.

    This function checks if a password meets the following criteria:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character

    :param password: The password string to validate.
    :type password: str
    :return: True if the password meets all criteria, otherwise False.
    :rtype: bool
    """
    # ---- Validate password length ----
    if not re.fullmatch(r'.{8,}', password):
        print("Password should be more than 8 characters")
        return False

    # ---- Validate presence of uppercase letter ----
    if not re.search(r'[A-Z]', password):
        print("Password should contain at least one uppercase letter")
        return False

    # ---- Validate presence of lowercase letter ----
    if not re.search(r'[a-z]', password):
        print("Password should contain at least one lowercase letter")
        return False

    # ---- Validate presence of a number ----
    if not re.search(r'[0-9]', password):
        print("Password should contain at least one number")
        return False

    # ---- Validate presence of a special character ----
    if not re.search(r'[!"\'#$%&()*+,\-./:;<=>?@\[\]\\^_`{|}~]', password):
        print("Password should contain at least one special character")
        return False

    print("Password is valid")
    return True


# ---- Test cases for password validation ----
assert validate_password('qwerty') is False
assert validate_password('qwerasdf') is False
assert validate_password('Qwerasdf') is False
assert validate_password('Qwerasdf1') is False
assert validate_password('Qwerasdf1!') is True
