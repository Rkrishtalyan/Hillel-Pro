"""Завдання 8: Перевірка успадкування та методів класу

Напишіть функцію analyze_inheritance(cls), яка приймає клас, аналізує його спадкування та виводить усі методи,
які він наслідує від базових класів."""

import inspect


def analyze_inheritance(cls):
    """
    Analyze inherited methods of a given class.

    This function compares the methods of a class with its base class and
    prints out the methods that are inherited but not magic methods.

    :param cls: The class to analyze for inheritance.
    :type cls: type
    """
    # child_methods = inspect.getmembers(cls, predicate=inspect.isfunction)
    # parent_methods = inspect.getmembers(cls.__base__, predicate=inspect.isfunction)
    # inherited_methods = [method for method in child_methods if method in parent_methods]
    # відмовився від ідєї бо ліньки було витягувати name з того що getmembers повертає
    inherited_methods = [
        method for method in dir(cls)
        if method in dir(cls.__base__) and not method.startswith("__")
    ]
    list_of_methods = "\n".join(
        f"- {method_name} з {cls.__base__.__name__}" for method_name in inherited_methods
    )
    print(f"Клас {cls.__name__} наслідує:\n{list_of_methods}")


class Parent:
    """
    Represent a parent class with a parent method.
    """

    def parent_method(self):
        """
        Parent method that does nothing.
        """
        pass


class Child(Parent):
    """
    Represent a child class inheriting from Parent with an additional child method.
    """

    def child_method(self):
        """
        Child method that does nothing.
        """
        pass


analyze_inheritance(Child)
