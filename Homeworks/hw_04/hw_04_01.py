"""
Завдання 1: Перевірка типів і атрибутів об'єктів.

Напишіть функцію analyze_object(obj), яка приймає будь-який об'єкт та виводить:
    - Тип об'єкта.
    - Список всіх методів та атрибутів об'єкта.
    - Тип кожного атрибута.
"""


class MyClass:
    """
    Represent a class with a single value attribute.

    :var value: The value to be used in the MyClass instance.
    :type value: str
    """

    def __init__(self, value):
        """
        Initialize the MyClass instance with a value.

        :param value: The value to be set for the instance.
        :type value: str
        """
        self.value = value

    def say_hello(self):
        """
        Return a greeting message using the value.

        :return: A formatted string greeting.
        :rtype: str
        """
        return f"Hello, {self.value}"


class MyOwnClass:
    """
    Represent a class with three attributes.

    :var attr_1: The first attribute of the object.
    :type attr_1: Any
    :var attr_2: The second attribute of the object.
    :type attr_2: Any
    :var attr_3: The third attribute of the object.
    :type attr_3: Any
    """

    def __init__(self, attr_1, attr_2, attr_3):
        """
        Initialize MyOwnClass instance with three attributes.

        :param attr_1: The first attribute to be set.
        :type attr_1: Any
        :param attr_2: The second attribute to be set.
        :type attr_2: Any
        :param attr_3: The third attribute to be set.
        :type attr_3: Any
        """
        self.attr_1 = attr_1
        self.attr_2 = attr_2
        self.attr_3 = attr_3

    def sample_method(self):
        """
        Print a sample message with object information.

        :return: None
        """
        print(f"This is a sample method for object {self}")


def analyze_object(obj):
    """
    Analyze an object's type and attributes.

    :param obj: The object to be analyzed.
    :type obj: Any
    :return: A string summarizing the object's type and attributes.
    :rtype: str
    """
    obj_type = type(obj)
    obj_details = "\n".join(f"- {el}, {type(getattr(obj, el))}" for el in dir(obj) if not el.startswith("__"))

    return (f"Object type:\n{obj_type}\n\n"
            f"Methods and attributes:\n{obj_details}\n")


a = {"a": 1, "b": 2}
b = MyClass("World")
c = MyOwnClass(1, "two", [3])

print(f"Object: a\n\n{analyze_object(a)}")
print(f"Object: b\n\n{analyze_object(b)}")
print(f"Object: c\n\n{analyze_object(c)}")
