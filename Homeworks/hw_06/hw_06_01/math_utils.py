__all__ = ['factorial', 'gcd']  # приховуємо декоратор від імпорту


def memoize(func):
    """
    Memoize the given function by caching its results.

    :param func: The function to be memoized.
    :type func: function
    :return: The memoized version of the function.
    :rtype: function
    """
    cache = {}

    def wrapper(*args):
        """
        Check if the arguments exist in the cache. If yes, return the cached value,
        otherwise compute the result and cache it.

        :param args: Arguments to the memoized function.
        :type args: tuple
        :return: Cached result or computed result of the function.
        :rtype: Any
        """
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


@memoize
def factorial(n):
    """
    Calculate the factorial of a number using recursion.

    :param n: Non-negative integer for which the factorial is to be computed.
    :type n: int
    :return: Factorial of the input number.
    :rtype: int
    """
    if n == 0:
        return 1
    return n * factorial(n - 1)


def gcd(m, n):
    """
    Compute the greatest common divisor (GCD) of two integers using subtraction-based Euclidean algorithm.

    :param m: First integer.
    :type m: int
    :param n: Second integer.
    :type n: int
    :return: The greatest common divisor of m and n.
    :rtype: int
    """
    while m != n:
        if m > n:
            m = m - n
        else:
            n = n - m
    return n
