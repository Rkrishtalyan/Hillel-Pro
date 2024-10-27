"""
Завдання 2. Пошук телефонних номерів.

Напишіть функцію, яка знаходить усі телефонні номери в тексті. Номери можуть бути в форматах:

-   (123) 456-7890
-   123-456-7890
-   123.456.7890
-   1234567890
"""

import re


def find_phone(text):
    """
    Find all phone numbers in a given text.

    This function searches for phone numbers by sanitizing the text to remove non-alphanumeric characters,
    then matching sequences of exactly 10 digits.

    :param text: The text to search for phone numbers.
    :type text: str
    :return: A list of phone numbers found in the text.
    :rtype: list of str
    """
    sanitized_text = re.sub(r'[^\w]', '', text)
    phones = re.findall(r'\d{10}', sanitized_text)
    return phones


# ---- Define sample text and test the phone finder ----
text = '''Завдання 2. Пошук телефонних номерів
Напишіть функцію, яка знаходить усі телефонні номери в тексті. Номери можуть бути в форматах:

(123) 456-7890
123-456-7890
123.456.7890
1234567890'''

print(find_phone(text))
