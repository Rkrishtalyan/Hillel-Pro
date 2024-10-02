"""
Завдання 4: Створення класу динамічно.

Напишіть функцію create_class(class_name, methods), яка створює клас з заданим іменем та методами.
Методи передаються у вигляді словника, де ключі — це назви методів, а значення — функції.
"""


def create_class(class_name, methods_list):
    """
    Create a new class dynamically.

    This function uses the `type` function to dynamically create a class
    with the specified name and methods.

    :param class_name: The name of the class to be created.
    :type class_name: str
    :param methods_list: A dictionary of method names and functions for the class.
    :type methods_list: dict
    :return: A dynamically created class.
    :rtype: type
    """
    return type(class_name, (object,), methods_list)


def say_hello(self):
    """
    Return a greeting message.

    This method returns a simple 'Hello!' message.

    :return: A greeting message.
    :rtype: str
    """
    return "Hello!"


def say_goodbye(self):
    """
    Return a farewell message.

    This method returns a simple 'Goodbye!' message.

    :return: A farewell message.
    :rtype: str
    """
    return "Goodbye!"


methods = {
    "say_hello": say_hello,
    "say_goodbye": say_goodbye
}

MyDynamicClass = create_class("MyDynamicClass", methods)

obj = MyDynamicClass()
print(obj.say_hello())  # Hello!
print(obj.say_goodbye())  # Goodbye!
