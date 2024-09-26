"""1. Dunder methods.

1.	Реалізуйте клас Fraction (дробові числа), який має методи для додавання, віднімання, множення
    та ділення двох об'єктів цього класу. Використайте спеціальні методи __add__, __sub__, __mul__, __truediv__.
2.	Реалізуйте метод __repr__, щоб можна було коректно виводити об'єкти цього класу у форматі "numerator/denominator".
"""


class Fraction:
    """Represent a fraction with a numerator and denominator."""

    def __init__(self, numerator, denominator):
        """Initialize the Fraction instance.

        Args:
            numerator (int): The numerator of the fraction.
            denominator (int): The denominator of the fraction.

        Raises:
            ValueError: If the denominator is zero.
        """
        if denominator == 0:
            raise ValueError("Denominator cannot be zero.")
        self.numerator = numerator
        self.denominator = denominator

    def __add__(self, other):
        """Add two fractions and return the result.

        Args:
            other (Fraction): The fraction to add.

        Returns:
            Fraction: The sum of the two fractions.
        """
        result_numerator = (self.numerator * other.denominator) + (other.numerator * self.denominator)
        result_denominator = self.denominator * other.denominator
        return Fraction(result_numerator, result_denominator)

    def __sub__(self, other):
        """Subtract another fraction from this one and return the result.

        Args:
            other (Fraction): The fraction to subtract.

        Returns:
            Fraction: The difference between the two fractions.
        """
        result_numerator = (self.numerator * other.denominator) - (other.numerator * self.denominator)
        result_denominator = self.denominator * other.denominator
        return Fraction(result_numerator, result_denominator)

    def __mul__(self, other):
        """Multiply two fractions and return the product.

        Args:
            other (Fraction): The fraction to multiply.

        Returns:
            Fraction: The product of the two fractions.
        """
        result_numerator = self.numerator * other.numerator
        result_denominator = self.denominator * other.denominator
        return Fraction(result_numerator, result_denominator)

    def __truediv__(self, other):
        """Divide this fraction by another and return the quotient.

        Args:
            other (Fraction): The fraction to divide by.

        Returns:
            Fraction: The quotient of the two fractions.

        Raises:
            ValueError: If the other fraction's numerator is zero.
        """
        if other.numerator == 0:
            raise ValueError("Cannot divide by a fraction with a numerator of zero.")
        result_numerator = self.numerator * other.denominator
        result_denominator = self.denominator * other.numerator
        return Fraction(result_numerator, result_denominator)

    def __repr__(self):
        """Return the official string representation of the fraction.

        Returns:
            str: A string that can be used to recreate the fraction.
        """
        return f'{self.numerator}/{self.denominator}'


f1 = Fraction(2, 3)
f2 = Fraction(3, 5)

print(f"Addition: {f1} + {f2} = {f1 + f2}")
print(f"Subtraction: {f1} - {f2} = {f1 - f2}")
print(f"Multiplication: {f1} * {f2} = {f1 * f2}")
print(f"Division: {f1} / {f2} = {f1 / f2}")
