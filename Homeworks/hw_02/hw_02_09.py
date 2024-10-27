"""
Завдання 9: Кешування результатів функції.

Написати програму для кешування результатів функції, щоб покращити продуктивність.

1.  Створити функцію memoize, яка приймає функцію та повертає нову функцію,
    що зберігає результати викликів.
2.  Використати цю функцію, щоб кешувати результати обчислень
    (наприклад, факторіал або фібоначі).
"""

from time import time


# ---- Define memoization decorator ----
def memoize(func):
    """
    Cache the results of a function to avoid redundant computations.

    The decorator stores previously computed results in a dictionary, using the
    function arguments as keys. If a function call with the same arguments
    occurs, the cached result is returned.

    :param func: Function to be memoized.
    :type func: function
    :return: Memoized function that uses cached results if available.
    :rtype: function
    """
    cache = {}

    def wrapper(*args):
        """
        Wrapper function to handle caching.

        Checks if the arguments are already in the cache. If they are, returns
        the cached result; otherwise, computes the result, caches it, and returns it.

        :param args: Arguments to pass to the memoized function.
        :type args: tuple
        :return: Result of the function call.
        """
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return wrapper


# ---- Define memoized recursive functions ----
@memoize
def fibonacci(n):
    """
    Calculate the nth Fibonacci number using recursion and memoization.

    :param n: Position in the Fibonacci sequence.
    :type n: int
    :return: The nth Fibonacci number.
    :rtype: int
    """
    if n < 2:
        return n
    else:
        return fibonacci(n - 2) + fibonacci(n - 1)


@memoize
def factorial(n):
    """
    Calculate the factorial of n using recursion and memoization.

    :param n: Number to calculate the factorial for.
    :type n: int
    :return: The factorial of n.
    :rtype: int
    """
    if n == 0:
        return 1
    return n * factorial(n - 1)


# ---- Execute and measure function performance ----
fib_start = time()
print(fibonacci(120))
fib_end = time()

fac_start = time()
print(factorial(60))
fac_end = time()

print(f"Fibonacci calculation time: {fib_end - fib_start}")
print(f"Factorial calculation time: {fac_end - fac_start}")
