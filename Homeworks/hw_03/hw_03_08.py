"""
8. Price class discussion before the PaymentGateway implementation

1.  Реалізуйте клас Price, що представляє ціну товару з можливістю заокруглення до двох десяткових знаків.
    Додайте методи для додавання, віднімання та порівняння цін.
2.  Поміркуйте, як клас Price може бути використаний в майбутньому класі PaymentGateway
    для обробки фінансових транзакцій.
"""


class PriceValue:
    """
    Descriptor class for managing the price value, ensuring it is stored as a
    rounded float.
    """

    def __get__(self, instance_self, instance_class):
        """
        Get the value of the price from the instance's dictionary.

        :param instance_self: The instance that owns the attribute.
        :type instance_self: object
        :param instance_class: The class owning the descriptor.
        :type instance_class: type
        :return: The price value or 0.00 if not set.
        :rtype: float
        """
        return instance_self.__dict__.get('_value', 0.00)

    def __set__(self, instance_self, value):
        """
        Set the price value after validating and rounding it.

        :param instance_self: The instance that owns the attribute.
        :type instance_self: object
        :param value: The value to be set, must be an int or float.
        :type value: int, float
        :raises TypeError: If value is not an int or float.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be int or float")
        rounded_value = round(float(value), 2)
        instance_self.__dict__['_value'] = rounded_value

    def __delete__(self, instance_self):
        """
        Delete the price value from the instance's dictionary.

        :param instance_self: The instance that owns the attribute.
        :type instance_self: object
        """
        del instance_self.__dict__['_value']


class Price:
    """
    Represents a price value, supports comparison and arithmetic operations.

    The Price class allows you to create and compare prices using various
    comparison operators and perform addition and subtraction on price instances.

    :var value: The price value.
    :type value: PriceValue
    """

    value = PriceValue()

    def __init__(self, amount):
        """
        Initialize a Price instance with a given amount.

        :param amount: The price amount to be set.
        :type amount: int, float
        """
        self.value = amount

    def __add__(self, other):
        """
        Add two Price objects.

        :param other: Another Price instance.
        :type other: Price
        :return: A new Price object with the sum of the two.
        :rtype: Price
        :raises NotImplementedError: If other is not a Price instance.
        """
        if not isinstance(other, Price):
            return NotImplemented
        return Price(self.value + other.value)

    def __sub__(self, other):
        """
        Subtract one Price from another.

        :param other: Another Price instance.
        :type other: Price
        :return: A new Price object with the difference.
        :rtype: Price
        :raises NotImplementedError: If other is not a Price instance.
        """
        if not isinstance(other, Price):
            return NotImplemented
        return Price(self.value - other.value)

    def __eq__(self, other):
        """
        Check if two Price objects are equal.

        :param other: Another Price instance.
        :type other: Price
        :return: True if the values are equal, otherwise False.
        :rtype: bool
        :raises NotImplementedError: If other is not a Price instance.
        """
        if not isinstance(other, Price):
            return NotImplemented
        return self.value == other.value

    def __gt__(self, other):
        """
        Check if this Price is greater than another.

        :param other: Another Price instance.
        :type other: Price
        :return: True if this Price is greater, otherwise False.
        :rtype: bool
        :raises NotImplementedError: If other is not a Price instance.
        """
        if not isinstance(other, Price):
            return NotImplemented
        return self.value > other.value

    def __lt__(self, other):
        """
        Check if this Price is less than another.

        :param other: Another Price instance.
        :type other: Price
        :return: True if this Price is less, otherwise False.
        :rtype: bool
        """
        return not self > other

    def __ne__(self, other):
        """
        Check if two Price objects are not equal.

        :param other: Another Price instance.
        :type other: Price
        :return: True if the values are not equal, otherwise False.
        :rtype: bool
        """
        return not self == other

    def __ge__(self, other):
        """
        Check if this Price is greater than or equal to another.

        :param other: Another Price instance.
        :type other: Price
        :return: True if this Price is greater or equal, otherwise False.
        :rtype: bool
        """
        return any((self > other, self == other))

    def __le__(self, other):
        """
        Check if this Price is less than or equal to another.

        :param other: Another Price instance.
        :type other: Price
        :return: True if this Price is less or equal, otherwise False.
        :rtype: bool
        """
        return any((self < other, self == other))

    def __repr__(self):
        """
        Return a string representation of the Price.

        :return: String representing the Price instance.
        :rtype: str
        """
        return f"Price({self.value:.2f})"


class PaymentGateway:
    """
    Simulates a payment gateway that processes payments using Price objects.
    """

    @staticmethod
    def process_payment(payment_amount, payment_due):
        """
        Process the payment and return the change if the amount is sufficient.

        :param payment_amount: The payment amount given.
        :type payment_amount: Price
        :param payment_due: The due payment amount.
        :type payment_due: Price
        :return: The change amount.
        :rtype: Price
        :raises TypeError: If the arguments are not Price objects.
        :raises ValueError: If the payment amount is less than the due amount.
        """
        if not isinstance(payment_amount, Price) or not isinstance(payment_due, Price):
            raise TypeError("Values should be of a price format")

        if payment_amount < payment_due:
            raise ValueError("Insufficient funds")

        change_amount = payment_amount - payment_due
        return change_amount


price_1 = Price(10.456)
price_2 = Price(5.123)

print(price_1)
print(price_2)

total = price_1 + price_2
print(total)

difference = price_1 - price_2
print(difference)

print(price_1 > price_2)

# Testing PaymentGateway class with Price objects as parameters
order_1 = PaymentGateway.process_payment(price_1, price_2)
print(order_1)
