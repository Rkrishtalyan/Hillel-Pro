"""
Завдання 4. Форматування дати.

Напишіть функцію, яка перетворює дати з формату DD/MM/YYYY у формат YYYY-MM-DD.
"""

import re


def convert_date(date):
    """
    Convert a date from MM/DD/YYYY format to YYYY-MM-DD format.

    This function extracts the year, month, and day components from a date string
    and formats them as 'YYYY-MM-DD'.

    :param date: The date string in DD/MM/YYYY format.
    :type date: str
    :return: The reformatted date string in YYYY-MM-DD format.
    :rtype: str
    """
    year = re.search(r'\d{4}', date)
    month = re.search(r'\d{1,2}/(\d{1,2})', date)
    day = re.search(r'(\d{1,2})/\d{1,2}', date)
    return f'{year.group()}-{month.group(1).zfill(2)}-{day.group(1).zfill(2)}'


# ---- Test date conversion function ----
print(convert_date('27/10/2024'))
