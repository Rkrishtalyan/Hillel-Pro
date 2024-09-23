from time import time


def memoize(func):
    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper


@memoize
def fibonacci(n):
    if n < 2:
        return n
    else:
        return fibonacci(n-2) + fibonacci(n-1)


@memoize
def factorial(n):
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
