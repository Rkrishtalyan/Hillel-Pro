"""
Завдання 8. Перевірка на наявність шаблону в тексті.

Напишіть функцію, яка перевіряє, чи міститься у тексті рядок формату AB12CD34,
де A, B, C, D — великі літери, а 1, 2, 3, 4 — цифри.
"""

import re


def check_pattern(text):
    """
    Check if the text contains a specific pattern.

    This function searches for a pattern in the text that matches two uppercase letters,
    followed by two digits, two uppercase letters, and two more digits (e.g., 'AB12CD34').

    :param text: The text to search for the pattern.
    :type text: str
    :return: True if the pattern is found, otherwise False.
    :rtype: bool
    """
    if re.search(r'[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{2}', text):
        return True
    return False


# ---- Define test texts ----
text_1 = """
Some random text about nothing.. Oh, look! A pattern!
AB12CD3... Nah.. almost. Maybe next time.
"""

text_2 = """
Another random text.. But wait! What is it?
EF56GH78! Yes! This is my pattern!
"""

text_3 = """
IJKL9012 MN3456OP QRSTUVWX 78901234
"""

# ---- Run assertions to test the pattern checker ----
try:
    assert check_pattern(text_1) is False
    assert check_pattern(text_2) is True
    assert check_pattern(text_3) is False
    print("All tests passed!")
except AssertionError:
    print("Assertion Error: One of the tests failed.")
