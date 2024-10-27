"""
6.  Access-like

1.  Реалізуйте клас User з атрибутами first_name, last_name, email.
    Додайте методи для отримання та встановлення цих атрибутів через декоратор @property.
2.  Додайте методи для перевірки формату email-адреси.
"""

import re


class User:
    """
    Represent a user with a first name, last name, and email.

    The User class allows managing user details such as the first name,
    last name, and email. It also validates the email format.

    :var __first_name: The first name of the user.
    :type __first_name: str
    :var __last_name: The last name of the user.
    :type __last_name: str
    :var __email: The email of the user.
    :type __email: str
    """

    def __init__(self, first_name, last_name, email):
        """
        Initialize a User instance with first name, last name, and email.

        :param first_name: The first name of the user.
        :type first_name: str
        :param last_name: The last name of the user.
        :type last_name: str
        :param email: The email address of the user.
        :type email: str
        """
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email

    @property
    def first_name(self):
        """
        Get the first name of the user.

        :return: The first name of the user.
        :rtype: str
        """
        return self.__first_name

    @first_name.setter
    def first_name(self, new_first_name):
        """
        Set a new first name for the user.

        :param new_first_name: The new first name to be set.
        :type new_first_name: str
        """
        self.__first_name = new_first_name

    # альтернативний варыант використання
    last_name = property()

    @last_name.getter
    def last_name(self):
        """
        Get the last name of the user.

        :return: The last name of the user.
        :rtype: str
        """
        return self.__last_name

    @last_name.setter
    def last_name(self, new_last_name):
        """
        Set a new last name for the user.

        :param new_last_name: The new last name to be set.
        :type new_last_name: str
        """
        self.__last_name = new_last_name

    # ще один альтернативний варыант
    def get_email(self):
        """
        Get the email address of the user.

        :return: The email address of the user.
        :rtype: str
        """
        return self.__email

    def set_email(self, new_email):
        """
        Set a new email for the user after validating its format.

        :param new_email: The new email address to be set.
        :type new_email: str
        :raises ValueError: If the email format is invalid.
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
            raise ValueError("Invalid email address format")
        self.__email = new_email

    email = property(get_email, set_email, None, "User's email address")

    def is_valid_email(self):
        """
        Check if the user's email is valid.

        :return: True if the email is valid, otherwise False.
        :rtype: bool
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            return False
        return True


person_1 = User('Ruslan', 'K', 'some_email_address@gmail.com')

print(f"First name: {person_1.first_name}")
print(f"Last name: {person_1.last_name}")
print(f"Email: {person_1.email}")

print()
print(f"Email address format is valid: {person_1.is_valid_email()}")

print()
person_1.first_name = "Bogdan"
person_1.last_name = "Y"
print(f"First name: {person_1.first_name}")
print(f"Last name: {person_1.last_name}")

try:
    person_1.email = "new_email_test.com"
except ValueError:
    print("ValueError: Invalid email address format")
else:
    assert False, "email.setter doesn't raise ValueError when expected"
