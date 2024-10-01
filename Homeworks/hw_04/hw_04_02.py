"""
Завдання 2: Динамічний виклик функцій

Реалізуйте функцію call_function(obj, method_name, *args), яка приймає об'єкт, назву методу в вигляді рядка
та довільні аргументи для цього методу. Функція повинна викликати відповідний метод об'єкта і повернути результат.
"""


def call_function(obj, method_name, *args):
    """
    Call a method on the given object using the method name and optional arguments.

    :param obj: The object on which to call the method.
    :type obj: object
    :param method_name: The name of the method to call on the object.
    :type method_name: str
    :param args: Additional positional arguments to pass to the method.
    :type args: any
    :return: The result of the method call.
    :rtype: any
    """
    return getattr(obj, method_name)(*args)


class Calculator:
    """
    Represent a simple calculator with basic arithmetic operations.

    The Calculator class provides methods for addition and subtraction.
    """

    def add(self, a, b):
        """
        Add two numbers and return the result.

        :param a: The first number to add.
        :type a: int or float
        :param b: The second number to add.
        :type b: int or float
        :return: The sum of a and b.
        :rtype: int or float
        """
        return a + b

    def subtract(self, a, b):
        """
        Subtract the second number from the first and return the result.

        :param a: The number to subtract from.
        :type a: int or float
        :param b: The number to subtract.
        :type b: int or float
        :return: The difference between a and b.
        :rtype: int or float
        """
        return a - b


calc = Calculator()
print(call_function(calc, "add", 10, 5))  # 15
print(call_function(calc, "subtract", 10, 5))  # 5
