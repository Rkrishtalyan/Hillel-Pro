"""
Завдання 10: Метаклас для контролю створення класів

Реалізуйте метаклас SingletonMeta, який гарантує, що клас може мати лише один екземпляр (патерн Singleton).
Якщо екземпляр класу вже створений, наступні виклики повинні повертати той самий об'єкт.
"""


class SingletonMeta(type):
    """
    Metaclass for implementing the Singleton design pattern.

    Ensures that only one instance of a class is created, storing it in
    a dictionary of instances. New instances are only created if none exist.

    :var _instances: Dictionary that holds the single instance of each class
                     using this metaclass.
    :type _instances: dict
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Call method that ensures only one instance of a class is created.

        If no instance exists for the class, it creates one and stores it in
        the _instances dictionary. Otherwise, it returns the already existing
        instance.

        :param args: Positional arguments passed to the class constructor.
        :param kwargs: Keyword arguments passed to the class constructor.
        :return: The singleton instance of the class.
        """
        if cls not in cls._instances:
            # If no instance exists, create and store it
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        # Return the stored instance (singleton behavior)
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    """
    Class that uses SingletonMeta to enforce a single instance.

    This class will only have one instance, regardless of how many
    times it is instantiated.
    """

    def __init__(self):
        """
        Initialize the Singleton instance.

        Prints a message to indicate instance creation.
        """
        print("Creating instance")


obj1 = Singleton()  # Creating instance
obj2 = Singleton()
print(obj1 is obj2)  # True
