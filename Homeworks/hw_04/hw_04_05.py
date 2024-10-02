"""
Завдання 5: Модифікація атрибутів під час виконання/].

Напишіть клас MutableClass, який має методи для динамічного додавання та видалення атрибутів об'єкта.
Реалізуйте методи add_attribute(name, value) та remove_attribute(name).
"""


class MutableClass:
    """
    Represent a class that allows dynamic attribute manipulation.

    This class allows adding and removing attributes dynamically at runtime.
    """

    def __init__(self):  # не обовʼязково, але PyCharm робив зауваження за 55 рядок

        """
        Initialize a MutableClass instance with an empty name attribute.

        :var name: Attribute to store a name, initially set to None.
        :type name: None
        """
        self.name = None

    def add_attribute(self, name, value):
        """
        Add or update an attribute to the instance.

        This method uses `setattr` to dynamically add a new attribute or update
        an existing one.

        :param name: Name of the attribute to add or update.
        :type name: str
        :param value: Value to assign to the attribute.
        :type value: any
        """
        setattr(self, name, value)

    def remove_attribute(self, name):
        """
        Remove an attribute from the instance.

        This method uses `delattr` to remove the specified attribute from the instance.

        :param name: Name of the attribute to remove.
        :type name: str
        :raises AttributeError: If the attribute does not exist.
        """
        delattr(self, name)


obj = MutableClass()

obj.add_attribute("name", "Python")
print(obj.name)  # Python

obj.remove_attribute("name")
# print(obj.name)  # Виникне помилка, атрибут видалений

try:
    print(obj.name)
except AttributeError:
    print("No attributes to display")
