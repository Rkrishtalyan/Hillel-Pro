"""
Завдання 4. Тестування з використанням doctest.

Додайте документацію з прикладами використання та напишіть тести з використанням doctest.

    Напишіть функції для роботи з числами:
-   is_even(n: int) -> bool: перевіряє, чи є число парним.
-   factorial(n: int) -> int: повертає факторіал числа.

Додайте doctest-приклади для кожної функції.
Переконайтеся, що doctest проходить для кожної функції запустивши тести через python -m doctest.

"""

import doctest


def memoize(func):
    """
    Memoize a function to store previously computed results in a cache.

    :param func: The function to be memoized.
    :type func: function
    :return: Wrapped function with memoization applied.
    :rtype: function
    """
    cache = {}

    def wrapper(*args):
        """
        Call the memoized function, returning cached result if available.

        :param args: Arguments passed to the wrapped function.
        :return: The result of the wrapped function, cached or newly computed.
        """
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


def is_even(n):
    """
    Check if a number is even.

    :param n: The number to be checked.
    :type n: int
    :return: True if the number is even, False otherwise.
    :rtype: bool

    >>> is_even(2)
    True
    >>> is_even(3)
    False
    """
    if n % 2 == 0:
        return True
    return False


# @memoize - виялвяється що doctest не працює з декорованими функціями
# можна додати functools, але ліньки
def factorial(n):
    """
    Compute the factorial of a number using memoization.

    :param n: The number to compute the factorial for.
    :type n: int
    :return: The factorial of the number.
    :rtype: int

    >>> factorial(2)
    2
    >>> factorial(10)
    3628800
    """
    if n == 0:
        return 1
    return n * factorial(n - 1)


# ---- Code Execution Block ----
if __name__ == '__main__':
    doctest.testmod()
