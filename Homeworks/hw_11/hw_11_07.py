"""
Завдання 7: Порівняння багатопотоковості/багатопроцесорності/асинхронності.

Реалізуйте та дослідіть виконання 500 запитів за допомогою синхронного/багатопотокового/
багатопроцесорного/асинхронного режимів за часом.
"""

import threading
import multiprocessing
import asyncio

import time
import math
import requests
import aiohttp


# ---- Define URL Processing Function ----
def process_urls(urls):
    """
    Process a list of URLs and print the first 10 characters of each response.

    :param urls: List of URLs to be processed.
    :type urls: list
    """
    for n, url in enumerate(urls, 1):
        response = requests.get(url, timeout=10)
        print(f"{n}: {response.text[0:10]}")


# ---- Synchronous URL Processing ----
def use_sync(urls):
    """
    Perform synchronous processing of URLs.

    :param urls: List of URLs to be processed.
    :type urls: list
    :return: Elapsed time for synchronous processing.
    :rtype: float
    """
    number_of_urls = len(urls)

    print("-------- Sync test started --------")
    print(f"Number of URLs: {number_of_urls}\n")
    start = time.perf_counter()

    process_urls(urls)

    elapsed_time = time.perf_counter() - start
    print(f"Sync test finished. Elapsed time {elapsed_time:0.2f} seconds\n")
    return elapsed_time


# ---- Threaded URL Processing ----
def use_threading(urls):
    """
    Perform URL processing using threading for parallel execution.

    :param urls: List of URLs to be processed.
    :type urls: list
    :return: Elapsed time for threaded processing.
    :rtype: float
    """
    number_of_urls = len(urls)
    num_threads = 4
    chunk_size = math.ceil(number_of_urls / num_threads)
    chunks = []

    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = start_index + chunk_size
        chunk = urls[start_index:end_index]
        if chunk:
            chunks.append(chunk)

    threads = []

    for chunk in chunks:
        thread = threading.Thread(target=process_urls, args=(chunk,))
        threads.append(thread)

    print("-------- Thread test started --------")
    print(f"Number of URLs: {number_of_urls}")
    print(f"Number of threads: {num_threads}\n")
    start_time = time.perf_counter()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    elapsed_time = time.perf_counter() - start_time
    print(f"Thread test finished. Elapsed time {elapsed_time:0.2f} seconds\n")
    return elapsed_time


# ---- Multiprocessing URL Processing ----
def use_multiprocessing(urls):
    """
    Perform URL processing using multiprocessing for parallel execution.

    :param urls: List of URLs to be processed.
    :type urls: list
    :return: Elapsed time for multiprocessing.
    :rtype: float
    """
    number_of_urls = len(urls)
    num_processes = multiprocessing.cpu_count()
    chunk_size = math.ceil(number_of_urls / num_processes)

    chunks = []

    for i in range(num_processes):
        start_index = i * chunk_size
        end_index = start_index + chunk_size
        chunk = urls[start_index:end_index]
        if chunk:
            chunks.append(chunk)

    with multiprocessing.Pool(processes=num_processes) as pool:
        print("-------- Pool test started --------")
        print(f"Number of URLs: {number_of_urls}")
        print(f"Number of processes: {num_processes}\n")
        start = time.perf_counter()

        pool.map(process_urls, chunks)

        elapsed_time = time.perf_counter() - start
        print(f"Pool test finished. Elapsed time {elapsed_time:0.2f} seconds.\n")

    return elapsed_time


# ---- Async URL Processing ----
async def get_async_response(session, url):
    """
    Get the first 10 characters of the asynchronous response from a URL.

    :param session: Aiohttp session for async requests.
    :type session: aiohttp.ClientSession
    :param url: URL to fetch the response from.
    :type url: str
    :return: First 10 characters of the response.
    :rtype: str
    """
    async with session.get(url) as response:
        result = await response.text()
        return result[0:10]


async def use_async(urls):
    """
    Perform asynchronous processing of URLs.

    :param urls: List of URLs to be processed.
    :type urls: list
    :return: Elapsed time for async processing.
    :rtype: float
    """
    number_of_urls = len(urls)

    print("-------- Async test started --------")
    print(f"Number of URLs: {number_of_urls}\n")
    start = time.perf_counter()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(get_async_response(session, url))
            tasks.append(task)
        results = await asyncio.gather(*tasks, return_exceptions=True)

    for n, task in enumerate(results, 1):
        print(f"{n}: {task}")

    elapsed_time = time.perf_counter() - start
    print(f"Async test finished. Elapsed time {elapsed_time:0.2f} seconds.\n")
    return elapsed_time


# ---- Main Execution Block ----
if __name__ == "__main__":
    num_urls = 500
    urls = ["https://www.example.com"] * num_urls

    sync_time = use_sync(urls)
    threading_time = use_threading(urls)
    multiprocessing_time = use_multiprocessing(urls)
    async_time = asyncio.run(use_async(urls))

    print("-------- Final results --------")
    print(f"Synchronicity: {sync_time:0.2f} seconds.")
    print(f"Multithreading: {threading_time:0.2f} seconds.")
    print(f"Multiprocessing: {multiprocessing_time:0.2f} seconds.")
    print(f"Asyncronicity: {async_time:0.2f} seconds.")

# -------- Final results --------
# Synchronicity: 384.75 seconds.
# Multithreading: 96.36 seconds.
# Multiprocessing: 49.38 seconds.
# Asyncronicity: 1.70 seconds.
