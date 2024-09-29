"""
7. Vector class implementation

1.  Створіть клас Vector, який представляє вектор у просторі з n вимірами. Додайте методи для додавання,
    віднімання векторів та обчислення скалярного добутку. Використовуйте dunder-методи (__add__, __sub__, __mul__).
2.  Додайте можливість порівняння двох векторів за їх довжиною.
"""

from math import sqrt


class Vector:
    """
    Represent a vector in a multidimensional space.

    :var coordinates: The coordinates of the vector.
    :type coordinates: tuple
    :var dimension: The dimension of the vector.
    :type dimension: int
    """

    def __init__(self, coordinates):
        """
        Initialize a Vector instance with given coordinates.

        :param coordinates: A list or tuple of numeric values representing the vector's coordinates.
        :type coordinates: list or tuple
        :raises ValueError: If the coordinates are not provided or are empty.
        """
        if not coordinates:
            raise ValueError("Coordinates cannot be empty.")
        self.coordinates = tuple(coordinates)
        self.dimension = len(self.coordinates)

    def __add__(self, other):
        """
        Add two vectors if they have the same dimension.

        :param other: Another vector to add.
        :type other: Vector
        :return: A new vector that is the sum of self and other.
        :rtype: Vector
        :raises ValueError: If the vectors do not have the same dimension.
        """
        if self.dimension != other.dimension:
            raise ValueError("Vectors must have the same dimension to be added.")
        new_coordinates = [a + b for a, b in zip(self.coordinates, other.coordinates)]
        return Vector(new_coordinates)

    def __sub__(self, other):
        """
        Subtract one vector from another if they have the same dimension.

        :param other: Another vector to subtract from self.
        :type other: Vector
        :return: A new vector that is the difference of self and other.
        :rtype: Vector
        :raises ValueError: If the vectors do not have the same dimension.
        """
        if self.dimension != other.dimension:
            raise ValueError("Vectors must have the same dimension to be subtracted.")
        new_coordinates = [a - b for a, b in zip(self.coordinates, other.coordinates)]
        return Vector(new_coordinates)

    def __mul__(self, scalar):
        """
        Multiply the vector by a scalar.

        :param scalar: A number (int or float) to multiply the vector.
        :type scalar: int or float
        :return: A new vector that is the result of scalar multiplication.
        :rtype: Vector
        :raises TypeError: If the scalar is not an integer or float.
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError("Scalar must be an integer or float.")
        new_coordinates = [a * scalar for a in self.coordinates]
        return Vector(new_coordinates)

    def scalar_product(self, other):
        """
        Compute the scalar (dot) product of two vectors.

        :param other: Another vector to calculate the scalar product with.
        :type other: Vector
        :return: The scalar product of self and other.
        :rtype: float
        :raises ValueError: If the vectors do not have the same dimension.
        """
        if self.dimension != other.dimension:
            raise ValueError("Vectors must have the same dimension to compute scalar product.")
        return sum(a * b for a, b in zip(self.coordinates, other.coordinates))

    def get_length(self):
        """
        Calculate the length (magnitude) of the vector.

        :return: The length of the vector.
        :rtype: float
        """
        return sqrt(sum(a ** 2 for a in self.coordinates))

    def __eq__(self, other):
        """
        Check if two vectors are equal in length.

        :param other: Another vector or an integer to compare with.
        :type other: Vector or int
        :return: True if self and other are equal in length, False otherwise.
        :rtype: bool
        :raises TypeError: If comparison is attempted with non-Vector or non-integer types.
        """
        if isinstance(other, Vector):
            return self.get_length() == other.get_length()
        elif isinstance(other, int):
            return self.get_length() == other
        raise TypeError("Comparison is only supported with Vector instances or integers.")

    def __lt__(self, other):
        """
        Check if the vector is shorter than another vector or integer.

        :param other: Another vector or an integer to compare with.
        :type other: Vector or int
        :return: True if self is shorter than other, False otherwise.
        :rtype: bool
        :raises TypeError: If comparison is attempted with non-Vector or non-integer types.
        """
        if isinstance(other, Vector):
            return self.get_length() < other.get_length()
        elif isinstance(other, int):
            return self.get_length() < other
        raise TypeError("Comparison is only supported with Vector instances or integers.")

    def __repr__(self):
        """
        Return a string representation of the vector.

        :return: A string representing the vector.
        :rtype: str
        """
        return f"Vector({self.coordinates})"


v1 = Vector([1, 2, 3])
v2 = Vector([4, 5, 6])

# Check that vectors are initialized properly
assert v1.coordinates == (1, 2, 3), "Vector coordinates are not initialized correctly"
assert v1.dimension == 3, "Vector dimension is not initialized correctly"

# Test addition
v3 = v1 + v2
assert v3.coordinates == (5, 7, 9), "Vector addition failed"

# Test subtraction
v4 = v1 - v2
assert v4.coordinates == (-3, -3, -3), "Vector subtraction failed"

# Test scalar multiplication
v5 = v1 * 2
assert v5.coordinates == (2, 4, 6), "Multiplication by scalar failed"

# Test scalar product
dot = v1.scalar_product(v2)
assert dot == 32, "Scalar product calculation failed"

# Test vector length
length = v1.get_length()
assert round(length, 2) == 3.74, "Vector length calculation failed"


# Test equality and comparison
v6 = Vector([1, 2, 3])

# Check equality of vectors
assert v1 == v6, "Vectors equality check failed"

# Check inequality
assert v1 != v2, "Vectors inequality check failed"

# Check comparison with integer
assert round(v1.get_length(), 2) == 3.74, "Manual int comparison check failed"
assert v1 < 5, "Less then int comparison check failed"

# Test dimension mismatch handling
v7 = Vector([1, 2])

try:
    v1 + v7
except ValueError as message:
    assert str(message) == "Vectors must have the same dimension to be added.", "Dimension matching check failed"

try:
    v1.scalar_product(v7)
except ValueError as message:
    assert str(message) == "Vectors must have the same dimension to compute scalar product.", "Dot calculation failed"

print("All test cases passed!")
