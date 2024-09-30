"""
Завдання 1: Перевірка типів і атрибутів об'єктів.

Напишіть функцію analyze_object(obj), яка приймає будь-який об'єкт та виводить:
    - Тип об'єкта.
    - Список всіх методів та атрибутів об'єкта.
    - Тип кожного атрибута.
"""


class MyClass:
    """
    Represent a class with three attributes.

    :var attr_1: First attribute of the class.
    :type attr_1: any
    :var attr_2: Second attribute of the class.
    :type attr_2: any
    :var attr_3: Third attribute of the class.
    :type attr_3: any
    """

    def __init__(self, attr_1, attr_2, attr_3):
        """
        Initialize MyClass with three attributes.

        :param attr_1: The first attribute.
        :type attr_1: any
        :param attr_2: The second attribute.
        :type attr_2: any
        :param attr_3: The third attribute.
        :type attr_3: any
        """
        self.attr_1 = attr_1
        self.attr_2 = attr_2
        self.attr_3 = attr_3

    def test_method(self):
        """
        Print a test message indicating the object reference.
        """
        print(f"This is a test method for object {self}")


def analyze_object(obj):
    """
    Analyze an object's type, directory, and attributes.

    If the object has a __dict__, display its attributes along with their
    types and values. If not, indicate that the object has no attributes.

    :param obj: The object to be analyzed.
    :type obj: any
    :return: A formatted string describing the object's type, methods,
             and attributes.
    :rtype: str
    """
    obj_type = type(obj)
    obj_dir = dir(obj)
    obj_attrs = ""

    if hasattr(obj, "__dict__"):
        for key, value in obj.__dict__.items():
            obj_attrs += f"Attribute '{key}': value - {value}, type - {type(value)}\n"
    else:
        obj_attrs = "This object has no attributes to display\n"

    return (f"Object type:\n{obj_type}\n\n"
            f"Methods and attributes:\n{obj_dir}\n\n"
            f"Attribute types:\n{obj_attrs}\n")


a = {"a": 1, "b": 2}
b = MyClass(1, "two", [3])

print(analyze_object(a))
print(analyze_object(b))
