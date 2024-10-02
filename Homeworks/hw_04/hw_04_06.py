"""
Завдання 6: Інтерсепція методів класу (Proxy)

Напишіть клас Proxy, який приймає на вхід об'єкт і переадресовує виклики методів цього об'єкта,
додатково логуючи виклики (наприклад, виводячи назву методу та аргументи).
"""


class Proxy:
    """
    Proxy class that wraps another object and intercepts method calls.

    The Proxy class forwards attribute access to the wrapped instance. It also logs method
    calls with their parameters if the attribute is callable.

    :var instance: The instance to wrap and proxy method calls for.
    :type instance: object
    """

    def __init__(self, instance):
        """
        Initialize the Proxy with an instance to wrap.

        :param instance: The instance to be wrapped by the Proxy.
        :type instance: object
        """
        self.instance = instance

    def __getattr__(self, attr):
        """
        Intercept attribute access and handle callable attributes by wrapping them.

        If the attribute is a callable (like a method), it wraps the call and logs the
        parameters before delegating to the original method.

        :param attr: The name of the attribute being accessed.
        :type attr: str
        :return: The attribute from the wrapped instance or a wrapped method.
        :rtype: object
        """
        orig_attr = getattr(self.instance, attr)

        if callable(orig_attr):  # от завдання вивести аргументи прям зламало голову...
            def wrapper(*args):
                """
                Log method calls with their parameters and forward the call to the original method.

                :param args: Positional arguments passed to the method.
                :type args: tuple
                :return: The result of the original method call.
                :rtype: object
                """
                print(f"Calling method:\n'{attr}' with args: {args}")
                return orig_attr(*args)
            return wrapper
        return orig_attr


class MyClass:
    """
    Simple class with a greeting method.

    The MyClass class contains a method to return a greeting message.
    """

    def greet(self, name):
        """
        Return a greeting message.

        :param name: The name of the person to greet.
        :type name: str
        :return: A greeting message.
        :rtype: str
        """
        return f"Hello, {name}!"


obj = MyClass()
proxy = Proxy(obj)

print(proxy.greet("Alice"))
