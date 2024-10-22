"""
Задача 7: обчислення факторіалу великих чисел.

Напишіть програму, яка обчислює факторіал великого числа за допомогою декількох потоків
або процесів, розподіляючи обчислення між ними.
"""

import multiprocessing
import math


# ---- Compute partial product of range ----
def compute_partial_product(start, end):
    """
    Compute the product of a range of numbers.

    :param start: The starting number of the range.
    :type start: int
    :param end: The ending number of the range.
    :type end: int
    :return: The product of numbers from start to end.
    :rtype: int
    """
    return math.prod(range(start, end + 1))


# ---- Split range for multiprocessing ----
def split_range(end, num_splits):
    """
    Split a range of numbers into smaller ranges for multiprocessing.

    :param end: The ending number of the range.
    :type end: int
    :param num_splits: The number of splits for multiprocessing.
    :type num_splits: int
    :return: A list of tuples representing ranges to process.
    :rtype: list of tuples
    """
    total_numbers = end
    chunk_size = math.ceil(total_numbers / num_splits)
    ranges = []

    for i in range(num_splits):
        range_start = 1 + i * chunk_size
        range_end = min(range_start + chunk_size - 1, end)
        if range_start > end:
            break
        ranges.append((range_start, range_end))

    return ranges


# ---- Main execution ----
def main():
    """
    Main function to calculate factorial of a given number using multiprocessing.

    Prompts user input, validates the number, splits the range for parallel
    computation, and calculates the factorial using multiprocessing.
    """
    try:
        n = int(input("Enter a number n to calculate n!: "))
        if n < 0:
            raise ValueError("Factorial is only defined for non-negative integers.")
    except ValueError as error:
        print(f"Invalid input: {error}")
        return

    if n == 0 or n == 1:
        print(f"{n}! = 1")
        return

    num_processes = multiprocessing.cpu_count()
    ranges = split_range(n, num_processes)

    with multiprocessing.Pool(processes=num_processes) as pool:
        partial_products = pool.starmap(compute_partial_product, ranges)

    factorial = 1
    for partial_product in partial_products:
        factorial *= partial_product
    print(f"{n}! = {factorial}")


if __name__ == '__main__':
    main()
