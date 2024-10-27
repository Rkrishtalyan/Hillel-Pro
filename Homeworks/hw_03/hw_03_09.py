"""
9.  Порівняння сеттерів/геттерів, декоратора @property та дескрипторів.

Реалізуйте клас Product, який представляє товар з наступними атрибутами:
1.  name – назва товару (рядок).
2.  price – ціна товару (число з плаваючою комою).

Вам потрібно реалізувати три варіанти роботи з атрибутом price:

1.  Сеттери/геттери: реалізуйте методи get_price() і set_price(), які будуть дозволяти
    отримувати та встановлювати значення атрибута price. Додайте перевірку,
    що ціна не може бути від'ємною. Якщо ціна менше 0, викиньте виняток ValueError.
2.  Декоратор @property: використайте декоратор @property для створення властивості price.
    Також реалізуйте перевірку на від'ємне значення ціни.
3.  Дескриптори: створіть окремий клас дескриптора PriceDescriptor, який буде контролювати
    встановлення та отримання ціни. Додайте до класу Product атрибут price, що використовує
    дескриптор для перевірки ціни.
"""


class ProductWithGetSet:
    """
    Represent a product with explicit getter and setter methods for price.

    :var name: The name of the product.
    :type name: str
    :var __price: The price of the product (private).
    :type __price: float
    """

    def __init__(self, name, price):
        """
        Initialize a product with a name and a price.

        :param name: The name of the product.
        :type name: str
        :param price: The price of the product, must be non-negative.
        :type price: float
        :raises ValueError: If the price is negative.
        """
        if price < 0:
            raise ValueError("Price cannot be less than zero")
        self.name = name
        self.__price = price

    def get_price(self):
        """
        Get the price of the product.

        :return: The price of the product.
        :rtype: float
        """
        return self.__price

    def set_price(self, new_price):
        """
        Set a new price for the product.

        :param new_price: The new price of the product.
        :type new_price: float
        :raises ValueError: If the new price is negative.
        """
        if new_price < 0:
            raise ValueError("Price cannot be less than zero")
        self.__price = new_price


class ProductWithProperty:
    """
    Represent a product using Python's property decorator for price management.

    :var name: The name of the product.
    :type name: str
    :var __price: The price of the product (private).
    :type __price: float
    """

    def __init__(self, name, price):
        """
        Initialize a product with a name and a price.

        :param name: The name of the product.
        :type name: str
        :param price: The price of the product, must be non-negative.
        :type price: float
        :raises ValueError: If the price is negative.
        """
        if price < 0:
            raise ValueError("Price cannot be less than zero")
        self.name = name
        self.__price = price

    @property
    def price(self):
        """
        Get the price of the product.

        :return: The price of the product.
        :rtype: float
        """
        return self.__price

    @price.setter
    def price(self, new_price):
        """
        Set a new price for the product.

        :param new_price: The new price of the product.
        :type new_price: float
        :raises ValueError: If the new price is negative.
        """
        if new_price < 0:
            raise ValueError("Price cannot be less than zero")
        self.__price = new_price


class PriceManager:
    """
    Descriptor class to manage price with custom getter and setter logic.
    """

    def __get__(self, instance, owner):
        """
        Get the price value from an instance.

        :param instance: The instance that contains the price.
        :type instance: object
        :param owner: The class that owns the instance.
        :type owner: type
        :return: The price of the product, defaults to 0.00 if not set.
        :rtype: float
        """
        return instance.__dict__.get('_price', 0.00)

    def __set__(self, instance, new_price):
        """
        Set the price value for an instance.

        :param instance: The instance that contains the price.
        :type instance: object
        :param new_price: The new price to set for the product.
        :type new_price: float
        :raises ValueError: If the new price is negative.
        """
        if new_price < 0:
            raise ValueError("Price cannot be less than zero")
        instance.__dict__['_price'] = new_price


class ProductWithDescriptor:
    """
    Represent a product using a custom descriptor for price management.

    :var name: The name of the product.
    :type name: str
    :var price: The price of the product, managed by PriceManager.
    :type price: float
    """

    price = PriceManager()

    def __init__(self, name, price):
        """
        Initialize a product with a name and a price.

        :param name: The name of the product.
        :type name: str
        :param price: The price of the product, must be non-negative.
        :type price: float
        :raises ValueError: If the price is negative.
        """
        self.name = name
        self.price = price


# Creating instances
product_1 = ProductWithGetSet("Apple", 5)
product_2 = ProductWithProperty("Banana", 10)
product_3 = ProductWithDescriptor("Cherry", 7)

print(f"{product_1.name}, price: {product_1.get_price()}")
print(f"{product_2.name}, price: {product_2.price}")
print(f"{product_3.name}, price: {product_3.price}")


# Price change via respectful method/attribute
print()

product_1.set_price(product_1.get_price() + 1)
print(f"{product_1.name}, price: {product_1.get_price()}")

product_2.price += 1
print(f"{product_2.name}, price: {product_2.price}")

product_3.price += 1
print(f"{product_3.name}, price: {product_3.price}")


# Test of negative price change
print()

try:
    product_1.set_price(-5)
except ValueError as message:
    print(f"{product_1.name} price change to -5: {message}")

try:
    product_2.price = -10
except ValueError as message:
    print(f"{product_2.name} price change to -10: {message}")

try:
    product_3.price = -7
except ValueError as message:
    print(f"{product_2.name} price change to -7: {message}")


# Особисто мені на цьому етапі і у рамках цього завдання більше подобається property:
# - надає увесь необхідний функціонал для роботи із захищенними полями;
# - викликається через атрібут, а не як метод у випадку із ProductWithGetSet;
# - легша і зрозуміліша форма запису аніж у дескріптора.
# Проте, я розумію що у дескріптора більше можливостей, виходячи з доп.матеріалів. Можливо, дійдуть руки до додаткового
# завдання і там зміню свою думку.
