"""
Задача 3: підрахунок суми чисел у великому масиві
Створіть програму, яка ділить великий масив чисел на кілька частин
і рахує суму кожної частини паралельно в різних процесах.
Використовуйте модуль multiprocessing.
"""

import multiprocessing
import math
import random


# ---- Function Definitions ----

def chunk_sum(numbers):
    """
    Calculate the sum of a list of numbers.

    :param numbers: List of numbers to sum.
    :type numbers: list
    :return: The sum of the numbers.
    :rtype: int
    """
    return sum(numbers)


def split_array(numbers_array, num_chunks):
    """
    Split an array into a specified number of chunks.

    :param numbers_array: The array of numbers to split.
    :type numbers_array: list
    :param num_chunks: The number of chunks to split the array into.
    :type num_chunks: int
    :return: A list containing the split chunks.
    :rtype: list
    """
    chunk_size = math.ceil(len(numbers_array) / num_chunks)
    chunks = []

    for i in range(num_chunks):
        start_index = i * chunk_size
        end_index = start_index + chunk_size
        chunk = numbers_array[start_index:end_index]
        chunks.append(chunk)

    return chunks


# ---- Main Code Execution Section ----

if __name__ == '__main__':
    # large_array = [i for i in range(1, 1000001)]  # -> 500000500000
    large_array = [random.randint(1, 100) for _ in range(10000001)]
    num_cores = multiprocessing.cpu_count()

    # Split the array into chunks based on the number of cores
    chunks = split_array(large_array, num_cores)

    # Use multiprocessing to compute the sum of each chunk in parallel
    with multiprocessing.Pool(processes=num_cores) as pool:
        chunk_sums = pool.map(chunk_sum, chunks)

    # Calculate the total sum by summing all chunk results
    total_sum = sum(chunk_sums)

    print(f"The total sum is: {total_sum}")
