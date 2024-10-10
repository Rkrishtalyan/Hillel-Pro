"""
Завдання 3. Використання фікстур у pytest.

Напишіть програму для керування користувачами та напишіть тести з використанням фікстур у pytest.
Напишіть клас UserManager, який реалізує такі методи:

-   add_user(name: str, age: int): додає користувача.
-   remove_user(name: str): видаляє користувача на ім'я.
-   get_all_users() -> list: повертає список усіх користувачів.

Для тестів створіть фікстуру, яка попередньо додаватиме кількох користувачів
перед виконанням тестів.

Напишіть тести для перевірки методів add_user, remove_user, get_all_users.
Використовуйте фікстуру в кожному тесті для попереднього налаштування.

Створіть тест, який скипатиметься за певних умов
(наприклад, якщо у користувача менше трьох користувачів).
"""

import pytest


# ---- UserManager class definition ----
class UserManager:
    """
    Manage a collection of users with functionality to add, remove, and retrieve them.

    :var users: List of users, where each user is a dictionary with keys 'name' and 'age'.
    :type users: list
    """

    def __init__(self):
        """
        Initialize an empty list of users.
        """
        self.users = []

    def add_user(self, name, age):
        """
        Add a user to the user collection.

        :param name: The name of the user to be added.
        :type name: str
        :param age: The age of the user to be added.
        :type age: int
        """
        self.users.append({"name": name, "age": age})

    def remove_user(self, name):
        """
        Remove a user from the user collection by their name.

        :param name: The name of the user to be removed.
        :type name: str
        :return: The removed user's dictionary or None if the user is not found.
        :rtype: dict or None
        """
        for user in self.users:
            for i, user in enumerate(self.users):
                if user["name"] == name:
                    return self.users.pop(i)

        print("No user with such name found.")
        return None

    def get_all_users(self):
        """
        Get a list of all users in the collection.

        :return: A list of dictionaries representing users.
        :rtype: list
        """
        return [{"name": user["name"], "age": user["age"]} for user in self.users]


# ---- Pytest fixture definition ----
@pytest.fixture
def user_manager():
    """
    Provide a fixture for the UserManager instance pre-populated with test data.

    :return: A UserManager instance.
    :rtype: UserManager
    """
    um = UserManager()
    um.add_user("Alice", 30)
    um.add_user("Bob", 25)
    return um


# ---- Test functions ----
def test_add_user_fixture(user_manager):
    """
    Test adding a user to the user_manager fixture.
    """
    user_manager.add_user("Charlie", 22)
    assert len(user_manager.users) == 3
    assert user_manager.users[-1] == {"name": "Charlie", "age": 22}


def test_remove_user_fixture(user_manager):
    """
    Test removing a user from the user_manager fixture.
    """
    removed_user = user_manager.remove_user("Alice")
    assert removed_user == {"name": "Alice", "age": 30}
    assert len(user_manager.users) == 1
    assert {"name": "Alice", "age": 30} not in user_manager.users


def test_get_all_users_fixture(user_manager):
    """
    Test retrieving all users from the user_manager fixture.
    """
    users = user_manager.get_all_users()
    assert users == [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ]


def test_skip_if_less_than_three_users(user_manager):
    """
    Skip the test if there are less than three users in the user_manager fixture.
    """
    if len(user_manager.users) < 3:
        pytest.skip("Less than three users")

    user_manager.add_user("Charlie", 22)
    user_manager.add_user("David", 40)
    assert len(user_manager.users) >= 3
