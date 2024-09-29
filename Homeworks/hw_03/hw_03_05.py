"""
5. For built-in functions implementation

1.  Реалізуйте власну версію функцій len(), sum(), та min().
    Використовуйте спеціальні методи __len__, __iter__, __getitem__, якщо необхідно.
2.  Напишіть тест для кожної з реалізованих функцій.
"""


from collections.abc import Sequence


class MathCollection:
    """
    Represent a collection of mathematical data.

    Provides basic methods for iterating, summing, finding the minimum, and
    calculating the length of the collection.

    :var data: The sequence collection of data elements.
    :type data: Sequence
    """

    def __init__(self, data: Sequence):
        """
        Initialize the MathCollection with a sequence of data.

        :param data: A sequence collection of data elements.
        :type data: Sequence
        :raises TypeError: If the data is not a sequence.
        """
        if not isinstance(data, Sequence):
            raise TypeError(
                f"Object of type {type(data).__name__} must be a Sequence (e.g., list, tuple)"
            )
        self.data = data

    def __len__(self) -> int:
        """
        Return the length of the collection.

        :return: The number of elements in the collection.
        :rtype: int
        """
        return len(self.data)

    def __getitem__(self, index):
        """
        Retrieve an item from the collection by index.

        :param index: The index of the item to retrieve.
        :type index: int
        :return: The item at the specified index.
        """
        return self.data[index]

    def __iter__(self):
        """
        Return an iterator for the collection.

        :return: An iterator over the collection.
        :rtype: iterator
        """
        return iter(self.data)

    def my_len(self) -> int:
        """
        Calculate the length of the collection.

        :return: The length of the collection.
        :rtype: int
        """
        return len(self)

    def my_min(self):
        """
        Find the minimum value in the collection.

        :return: The minimum value in the collection.
        :raises ValueError: If the collection is empty.
        :rtype: int or float
        """
        if len(self) == 0:
            raise ValueError("Object is empty. Cannot calculate min value.")
        min_value = self.data[0]
        for item in self.data:
            if item < min_value:
                min_value = item
        return min_value

    def my_sum(self, start=0):
        """
        Calculate the sum of the collection elements, optionally starting with a specified value.

        :param start: The starting value for the sum, defaults to 0.
        :type start: int or float
        :return: The total sum of the collection elements.
        :rtype: int or float
        """
        total = start
        for item in self.data:
            total += item
        return total


mc_full = MathCollection([2, 3, 1, 4])
mc_empty = MathCollection([])
mc_type = MathCollection(2)

# Test my_len method
assert mc_full.my_len() > 1, "my_len method implementation issue for non-empty collections"
assert mc_empty.my_len() == 0, "my_len method implementation issue for empty collections"

# Test my_len method
assert mc_full.my_sum() == 10, "my_sum method calculation issue for non-empty collections"
assert mc_full.my_sum(15) == 25, "my_sum method implementation issue of 'start' parameter"
assert mc_empty.my_len() == 0, "my_sum method calculation issue for empty collections"

# Test my_min method
assert mc_full.my_min() == 1, "my_min method implementation issue for non-empty collections"

try:
    print(mc_empty.my_min())
except ValueError:
    pass
else:
    assert False, "ValueError is not raised when expected"

print("All tests passed!")
