"""
Завдання 5. Тестування винятків у pytest (опціонально)

Напишіть функцію divide(a: int, b: int) -> float, яка поділяє два числа.
Якщо знаменник дорівнює нулю, функція повинна викидати виняток ZeroDivisionError.

    Напишіть тести з використанням pytest, які:
-   перевіряють коректний поділ,
-   перевіряють викидання виключення ZeroDivisionError, якщо знаменник дорівнює нулю.

Додайте тест із параметризацією для перевірки поділу з різними значеннями.
"""

import pytest


# ---- Function Definitions ----

def divide(a, b):
    """
    Divide two numbers and raise an error if the divisor is zero.

    :param a: The numerator.
    :type a: float or int
    :param b: The denominator.
    :type b: float or int
    :return: The result of division.
    :rtype: float
    :raises ZeroDivisionError: If the denominator is zero.
    """
    if b == 0:
        raise ZeroDivisionError("Error: division by zero is not allowed")
    return a / b


# ---- Test Functions ----

def test_divide():
    """
    Test the divide function with normal cases and check if zero division raises an error.

    :return: None
    """
    assert divide(4, 2) == 2.0
    assert divide(10, 4) == 2.5

    with pytest.raises(ZeroDivisionError, match="Error: division by zero is not allowed"):
        divide(5, 0)


@pytest.mark.parametrize("m, n, result", [
    (100, 2, 50.0),
    (50, 4, 12.5),
    (3, 2, 1.5)
])
def test_divide_parametrized(m, n, result):
    """
    Test the divide function with multiple sets of parameters using pytest's parametrize feature.

    :param m: The numerator.
    :type m: float or int
    :param n: The denominator.
    :type n: float or int
    :param result: The expected result of the division.
    :type result: float
    :return: None
    """
    assert divide(m, n) == result
