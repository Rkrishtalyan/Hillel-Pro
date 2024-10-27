"""
Завдання 3. Видобування хеш-тегів з тексту.

Напишіть функцію, яка з тексту повертає список хеш-тегів.
Хеш-тег — це слово, що починається з #, і може включати лише букви та цифри.
"""

import re


def find_hashtags(text):
    """
    Find all hashtags in a given text.

    This function searches for hashtags by matching words that begin with a '#' symbol.

    :param text: The text to search for hashtags.
    :type text: str
    :return: A list of hashtags found in the text.
    :rtype: list of str
    """
    hashtags = re.findall(r'#\w+', text)
    return hashtags


# ---- Define sample text and test the hashtag finder ----
text = '''
Today, I dove deep into a #Python project that involves web scraping and data analysis. 
Leveraging libraries like BeautifulSoup and pandas made the process much smoother. 
Debugging some tricky issues was challenging, but the #programming community on forums 
provided invaluable support. Excited to see how this project evolves and enhances 
my #coding skills!

#Python #DataAnalysis
'''

print(find_hashtags(text))
