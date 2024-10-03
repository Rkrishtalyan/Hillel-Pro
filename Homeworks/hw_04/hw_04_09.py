"""
Завдання 9: Динамічне додавання властивостей

Напишіть клас DynamicProperties, в якому можна динамічно додавати властивості через методи. Використовуйте вбудовані
функції property() для створення геттера та сеттера під час виконання програми.
"""


class DynamicProperties:
    """
    Class to dynamically add properties to instances using the descriptor protocol.

    This class allows dynamic creation of properties for instances. Each property is
    protected through name mangling, preventing conflicts with other attributes
    in subclasses or other instances.
    """

    def add_property(self, key, value):
        """
        Add a property dynamically to the class instance.

        Creates a property using Python's descriptor protocol. The property
        is protected by name mangling and accessible through a getter and setter.

        :param key: The name of the property.
        :type key: str
        :param value: The initial value of the property.
        :type value: Any
        """
        protected_key = "_" + self.__class__.__name__ + "__" + key
        self.__dict__[protected_key] = value

        def get_attribute(obj):
            return obj.__dict__[protected_key]

        def set_attribute(obj, value):
            obj.__dict__[protected_key] = value

        setattr(self.__class__, key, property(get_attribute, set_attribute))


class DynamicPropertiesAlternative:
    """
    Class to dynamically add properties using a dictionary to store attributes.

    This class manages dynamic properties by storing them in an internal dictionary.
    It creates a getter and setter for each property to facilitate access and modification.
    """

    def __init__(self):
        """
        Initialize the class with an empty properties' dictionary.

        This dictionary will store properties dynamically added to the class.

        :var __properties: A dictionary to store dynamic properties.
        :type __properties: dict
        """
        self.__properties = {}

    def add_property(self, key, value):
        """
        Add a property dynamically to the class instance using a dictionary.

        This method uses a dictionary to manage the dynamic properties and
        creates a getter and setter for accessing and modifying the property.

        :param key: The name of the property.
        :type key: str
        :param value: The initial value of the property.
        :type value: Any
        """
        self.__properties[key] = value

        def get_attribute(obj):
            return obj.__properties[key]

        def set_attribute(obj, value):
            obj.__properties[key] = value

        setattr(self.__class__, key, property(get_attribute, set_attribute))


# Using direct attributes assignment
obj = DynamicProperties()

obj.add_property('name', 'default_name')
print(obj.name)  # default_name

obj.name = "Python"
print(obj.name)  # Python

# Using properties dictionary
obj_2 = DynamicPropertiesAlternative()

obj_2.add_property('name', 'default_name')
print(obj_2.name)  # default_name

obj_2.name = "Python"
print(obj_2.name)  # Python
