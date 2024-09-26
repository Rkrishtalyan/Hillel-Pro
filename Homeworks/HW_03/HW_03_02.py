"""2. Numeric-like.

1.	Реалізуйте клас Vector, що підтримує операції додавання, віднімання, множення на число та порівняння за довжиною.
    Використовуйте відповідні dunder-методи (__add__, __sub__, __mul__, __lt__, __eq__).

2.	Додайте до класу метод для отримання довжини вектора."""

from math import sqrt


class Vector:
    """
    Represent a 2D vector with basic arithmetic and comparison operations.

    :var x: The x-coordinate of the vector.
    :type x: float
    :var y: The y-coordinate of the vector.
    :type y: float
    """

    def __init__(self, x, y):
        """
        Initialize the Vector instance.

        :param x: The x-coordinate of the vector.
        :type x: float
        :param y: The y-coordinate of the vector.
        :type y: float
        """
        self.x = x
        self.y = y

    def __add__(self, other):
        """
        Add two vectors.

        :param other: The vector to add.
        :type other: Vector
        :return: A new vector that is the sum of this vector and the other.
        :rtype: Vector
        """
        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector(new_x, new_y)

    def __sub__(self, other):
        """
        Subtract one vector from another.

        :param other: The vector to subtract.
        :type other: Vector
        :return: A new vector that is the difference of this vector and the other.
        :rtype: Vector
        """
        new_x = self.x - other.x
        new_y = self.y - other.y
        return Vector(new_x, new_y)

    def __mul__(self, scalar):
        """
        Multiply the vector by a scalar.

        :param scalar: The scalar value to multiply with.
        :type scalar: float
        :return: A new vector that is the result of scaling this vector by the scalar.
        :rtype: Vector
        """
        new_x = self.x * scalar
        new_y = self.y * scalar
        return Vector(new_x, new_y)

    def get_length(self):
        """
        Calculate the length (magnitude) of the vector.

        :return: The length of the vector.
        :rtype: float
        """
        return sqrt(self.x ** 2 + self.y ** 2)

    def __eq__(self, other):
        """
        Check if two vectors are equal based on their lengths or compare with an integer.

        :param other: The vector or integer to compare with.
        :type other: Vector | int
        :return: True if the vectors have the same length, or the length of this vector equals the integer, False otherwise.
        :rtype: bool
        :raises TypeError: If the other object is neither a Vector nor an int.
        """
        if isinstance(other, Vector):
            return self.get_length() == other.get_length()
        elif isinstance(other, int):
            return self.get_length() == other
        raise TypeError("Comparison is only supported with Vector instances or integers.")

    def __lt__(self, other):
        """
        Check if this vector is shorter than another vector or an integer.

        :param other: The vector or integer to compare with.
        :type other: Vector | int
        :return: True if this vector is shorter than the other vector, or its length is less than the integer, False otherwise.
        :rtype: bool
        :raises TypeError: If the other object is neither a Vector nor an int.
        """
        if isinstance(other, Vector):
            return self.get_length() < other.get_length()
        elif isinstance(other, int):
            return self.get_length() < other
        raise TypeError("Comparison is only supported with Vector instances or integers.")

    def __repr__(self):
        """
        Return a string representation of the vector.

        :return: A string representing the vector in the form 'Vector(x, y)'.
        :rtype: str
        """
        return f"Vector({self.x}, {self.y})"


# Test cases
a = Vector(1, 2)
b = Vector(4, 8)
c = Vector(4, 8)

print(f"Vectors addition: {a} + {b} = {a + b}")
print(f"Vectors subtraction: {a} - {b} = {a - b}")
print(f"Vectors subtraction: {b} - {a} = {b - a}")
print(f"Scalar multiplication: {a} * {3} = {a * 3}")
print(f"Vectors comparison: {a} < {b}: {a < b}")
print(f"Vectors comparison: {a} = {b}: {a == b}")
print(f"Vectors comparison: {b} = {c}: {b == c}")
print(f"Vectors comparison: {b} = {3}: {b == 3}")
