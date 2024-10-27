"""
Завдання 5. Видалення HTML-тегів.

Напишіть функцію, яка видаляє всі HTML-теги з тексту.
"""

import re


def remove_html_tags(html):
    """
    Remove HTML tags and extra whitespace from the provided HTML text.

    This function removes all HTML tags, extra blank lines, and excessive spaces or tabs
    from the given HTML content.

    :param html: The HTML content to clean.
    :type html: str
    :return: The cleaned text with HTML tags and extra whitespace removed.
    :rtype: str
    """
    text_no_html = re.sub(r'<.*?>', '', html, flags=re.DOTALL)
    text_no_blank_lines = re.sub(r'\n\s*\n', '\n', text_no_html)
    final_text = re.sub(r'[ \t]+', ' ', text_no_blank_lines)

    return final_text


# ---- Read HTML file and apply HTML tag removal ----
with open('draft.html', 'r', encoding='utf-8') as f:
    text = f.read()
    text = remove_html_tags(text)

# ---- Output cleaned text ----
print(text)
