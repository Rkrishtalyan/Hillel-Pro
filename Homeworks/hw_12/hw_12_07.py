"""
Завдання 7. Пошук IP-адрес.

Напишіть функцію, яка з тексту витягує всі IPv4-адреси.
IPv4-адреса складається з чотирьох чисел (від 0 до 255), розділених крапками.
"""

import re


def get_ip_addresses(text):
    """
    Extract all IP addresses from a given text.

    This function finds and returns all occurrences of IPv4 addresses in the text
    by matching patterns of the format 'X.X.X.X' where X is a 1-3 digit number.

    :param text: The text from which to extract IP addresses.
    :type text: str
    :return: A list of IP addresses found in the text.
    :rtype: list of str
    """
    addresses = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', text)
    return addresses


# ---- Define sample text and test the IP address extractor ----
text = """
Python is a versatile programming language widely used in web development, data analysis, 
and automation. For instance, a Python web server might listen on IP address `192.0.2.10` 
to handle incoming requests. When connecting to databases, Python applications might interact 
with servers at `198.51.100.20` and `203.0.113.30`. For internal services, it could use `192.0.2.50`,
and for local testing, developers often utilize `127.0.0.1`. With libraries like `socket` and `requests`,
Python makes it easy to work with these IP addresses seamlessly, 
enabling robust and efficient networked applications.
"""

print(get_ip_addresses(text))
