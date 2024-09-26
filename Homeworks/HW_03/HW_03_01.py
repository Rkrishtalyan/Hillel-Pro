"""
1. Dunder methods.

1)	Реалізуйте клас Fraction (дробові числа), який має методи для додавання, віднімання, множення
    та ділення двох об'єктів цього класу. Використайте спеціальні методи __add__, __sub__, __mul__, __truediv__.
2)	Реалізуйте метод __repr__, щоб можна було коректно виводити об'єкти цього класу у форматі "numerator/denominator".
"""


class Fraction:
    """
    Represent a fraction with a numerator and denominator.

    The Fraction class allows basic arithmetic operations and provides a
    string representation of the fraction.

    :var numerator: The numerator of the fraction.
    :type numerator: int
    :var denominator: The denominator of the fraction.
    :type denominator: int
    """

    def __init__(self, numerator, denominator):
        """
        Initialize the Fraction instance with numerator and denominator.

        :param numerator: The numerator of the fraction.
        :type numerator: int
        :param denominator: The denominator of the fraction.
        :type denominator: int

        :raises ValueError: If the denominator is zero.
        """
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        self.numerator = numerator
        self.denominator = denominator

    def __add__(self, other):
        """
        Add two fractions and return the result.

        :param other: The fraction to add to this fraction.
        :type other: Fraction
        :return: The sum of this fraction and the other.
        :rtype: Fraction
        """
        result_numerator = (self.numerator * other.denominator) + (other.numerator * self.denominator)
        result_denominator = self.denominator * other.denominator
        return Fraction(result_numerator, result_denominator)

    def __sub__(self, other):
        """
        Subtract another fraction from this one and return the result.

        :param other: The fraction to subtract from this fraction.
        :type other: Fraction
        :return: The difference between this fraction and the other.
        :rtype: Fraction
        """
        result_numerator = (self.numerator * other.denominator) - (other.numerator * self.denominator)
        result_denominator = self.denominator * other.denominator
        return Fraction(result_numerator, result_denominator)

    def __mul__(self, other):
        """
        Multiply two fractions and return the product.

        :param other: The fraction to multiply with this fraction.
        :type other: Fraction
        :return: The product of the two fractions.
        :rtype: Fraction
        """
        result_numerator = self.numerator * other.numerator
        result_denominator = self.denominator * other.denominator
        return Fraction(result_numerator, result_denominator)

    def __truediv__(self, other):
        """
        Divide this fraction by another and return the quotient.

        :param other: The fraction to divide by.
        :type other: Fraction
        :return: The quotient of this fraction divided by the other.
        :rtype: Fraction
        :raises ValueError: If the other fraction's numerator is zero.
        """
        if other.numerator == 0:
            raise ValueError("Cannot divide by a fraction with a numerator of zero.")
        result_numerator = self.numerator * other.denominator
        result_denominator = self.denominator * other.numerator
        return Fraction(result_numerator, result_denominator)

    def __repr__(self):
        """
        Return the official string representation of the fraction.

        :return: The fraction in the format 'numerator/denominator'.
        :rtype: str
        """
        return f'{self.numerator}/{self.denominator}'


f1 = Fraction(2, 3)
f2 = Fraction(3, 5)

print(f"Addition: {f1} + {f2} = {f1 + f2}")
print(f"Subtraction: {f1} - {f2} = {f1 - f2}")
print(f"Multiplication: {f1} * {f2} = {f1 * f2}")
print(f"Division: {f1} / {f2} = {f1 / f2}")
