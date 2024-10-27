"""
4.  Binary

1.  Реалізуйте клас BinaryNumber, який представляє двійкове число.
    Додайте методи для виконання двійкових операцій:
    AND (__and__), OR (__or__), XOR (__xor__) та NOT (__invert__).
2.  Напишіть тест для цих операцій.
"""


class BinaryNumber:
    """
    Represent a binary number with logical operations.

    The BinaryNumber class provides binary AND, OR, XOR, and NOT operations.

    :var value: The boolean representation of the binary number.
    :type value: bool
    """

    def __init__(self, value):
        """
        Initialize a BinaryNumber instance from the given value.

        :param value: The value to initialize as a binary number. It can be any type
                      that can be evaluated for truthiness (set, dict, list, tuple, str, etc.)
        :type value: Any
        """
        if isinstance(value, (set, dict, list, tuple, str)):
            self.value = bool(len(value))
        else:
            self.value = bool(value)

    def and_mtd(self, other):
        """
        Perform the logical AND operation with another BinaryNumber.

        :param other: The other BinaryNumber to perform the AND operation with.
        :type other: BinaryNumber
        :return: A new BinaryNumber instance with the result of the AND operation.
        :rtype: BinaryNumber
        :raises TypeError: If the operand is not an instance of BinaryNumber.
        """
        if isinstance(other, BinaryNumber):
            return BinaryNumber(self.value and other.value)
        else:
            raise TypeError("Operand must be an instance of BinaryNumber.")

    def or_mtd(self, other):
        """
        Perform the logical OR operation with another BinaryNumber.

        :param other: The other BinaryNumber to perform the OR operation with.
        :type other: BinaryNumber
        :return: A new BinaryNumber instance with the result of the OR operation.
        :rtype: BinaryNumber
        :raises TypeError: If the operand is not an instance of BinaryNumber.
        """
        if isinstance(other, BinaryNumber):
            return BinaryNumber(self.value or other.value)
        else:
            raise TypeError("Operand must be an instance of BinaryNumber.")

    def xor_mtd(self, other):
        """
        Perform the logical XOR operation with another BinaryNumber.

        :param other: The other BinaryNumber to perform the XOR operation with.
        :type other: BinaryNumber
        :return: A new BinaryNumber instance with the result of the XOR operation.
        :rtype: BinaryNumber
        :raises TypeError: If the operand is not an instance of BinaryNumber.
        """
        if isinstance(other, BinaryNumber):
            return BinaryNumber(self.value != other.value)
        else:
            raise TypeError("Operand must be an instance of BinaryNumber.")

    def not_mtd(self):
        """
        Perform the logical NOT operation on the current BinaryNumber.

        :return: A new BinaryNumber instance with the result of the NOT operation.
        :rtype: BinaryNumber
        """
        return BinaryNumber(not self.value)

    def __str__(self):
        """
        Return a string representation of the BinaryNumber.

        :return: '1' if the value is True, otherwise '0'.
        :rtype: str
        """
        return '1' if self.value else '0'

    def __repr__(self):
        """
        Return a formal string representation of the BinaryNumber instance.

        :return: A string that represents the BinaryNumber instance.
        :rtype: str
        """
        return f"BinaryNumber({str(self)})"


bn_true = BinaryNumber(True)
bn_false = BinaryNumber(False)
bn_non_empty = BinaryNumber([1, 2, 3])
bn_empty = BinaryNumber([])
bn_zero = BinaryNumber(0)
bn_one = BinaryNumber(1)

# Test and_mtd
assert bn_true.and_mtd(bn_one).value is True, "True AND True should be True"
assert bn_true.and_mtd(bn_zero).value is False, "True AND False should be False"
assert bn_false.and_mtd(bn_empty).value is False, "False AND False should be False"

# Test or_mtd
assert bn_true.or_mtd(bn_false).value is True, "True OR False should be True"
assert bn_false.or_mtd(bn_zero).value is False, "False OR False should be False"

# Test xor_mtd
assert bn_true.xor_mtd(bn_empty).value is True, "True XOR False should be True"
assert bn_true.xor_mtd(bn_non_empty).value is False, "True XOR True should be False"

# Test not_mtd
assert bn_true.not_mtd().value is False, "NOT True should be False"
assert bn_false.not_mtd().value is True, "NOT False should be True"

# Test with non-empty and empty collections
assert bn_non_empty.value is True, "Non-empty collection should be True"
assert bn_empty.value is False, "Empty collection should be False"

# Test with zero and one
assert bn_zero.value is False, "Zero should be False"
assert bn_one.value is True, "One should be True"

# Test error handling
try:
    bn_true.and_mtd([1, 2, 3])
except TypeError:
    pass
else:
    assert False, "TypeError not raised when expected"

print("All tests passed!")
