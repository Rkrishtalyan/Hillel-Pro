"""
Завдання 7: Декоратор для логування викликів методів.

Реалізуйте декоратор log_methods, який додається до класу
і логуватиме виклики всіх його методів (назва методу та аргументи).
"""


def log_methods(cls):
    """
    Decorate a class to log its method calls.

    Replaces the `__getattribute__` method to log when any method is called
    and the arguments passed to it.

    :param cls: The class to be decorated.
    :type cls: type
    :return: The decorated class.
    :rtype: type
    """
    def logger(self, attr):
        """
        Log calls to the class's methods, if the attribute is callable.

        :param self: Instance of the class.
        :type self: object
        :param attr: The attribute to retrieve.
        :type attr: str
        :return: The method with logging functionality or the attribute itself.
        :rtype: object
        """
        actual_attr = object.__getattribute__(self, attr)
        if callable(actual_attr):
            def logger_with_params(*args):
                """
                Log the method call with its arguments.

                :param args: Arguments passed to the method.
                :type args: tuple
                :return: The result of the method call.
                :rtype: object
                """
                print(f"Logging: {attr} called with {args}")
                return actual_attr(*args)
            return logger_with_params
        return actual_attr

    cls.__getattribute__ = logger
    return cls


@log_methods
class MyClass:
    test_attr = 'test'

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b


obj = MyClass()
print(obj.add(5, 3))  # Logging: add called with (5, 3)
print(obj.subtract(5, 3))  # Logging: subtract called with (5, 3)
print(obj.test_attr)
