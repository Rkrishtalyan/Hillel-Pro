"""
Завдання 9: Кешування результатів функції

Написати програму для кешування результатів функції, щоб покращити продуктивність.

1.	Створити функцію memoize, яка приймає функцію та повертає нову функцію, що зберігає результати викликів.
2.	Використати цю функцію, щоб кешувати результати обчислень (наприклад, факторіал або фібоначі).
"""

from time import time


def memoize(func):
    """Return wrapper function with caching capability."""
    cache = {}

    def wrapper(*args):
        """Store and return computed results. Compute, save and return new calculations."""
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper


@memoize
def fibonacci(n):
    """Compute the nth Fibonacci number."""
    if n < 2:
        return n
    else:
        return fibonacci(n-2) + fibonacci(n-1)


@memoize
def factorial(n):
    """Compute the factorial of n."""
    if n == 0:
        return 1
    return n * factorial(n - 1)


fib_start = time()
print(fibonacci(120))
fib_end = time()

fac_start = time()
print(factorial(60))
fac_end = time()

print(fib_end - fib_start)
print(fac_end - fac_start)
