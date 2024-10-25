"""
Завдання 1: Основи асинхронності.

Напишіть асинхронну функцію download_page(url: str),
яка симулює завантаження сторінки за допомогою asyncio.sleep().
Функція повинна приймати URL та "завантажувати" сторінку за випадковий проміжок часу
від 1 до 5 секунд.
Після завершення завантаження, функція повинна вивести повідомлення з URL і часом завантаження.
Напишіть асинхронну функцію main(urls: list), яка приймає список з декількох URL
і завантажує їх одночасно, використовуючи await для паралельного виконання функції download_page().
"""

import asyncio
import random


# ---- Function Definitions ----

async def download_page(url):
    """
    Simulate downloading a page by printing a retrieval message, waiting for a random load time,
    and returning a message indicating download completion.

    :param url: The URL of the page to download.
    :type url: str
    :return: A message indicating the page download completion and time spent.
    :rtype: str
    """
    print(f"Retrieving page from {url}")
    load_time = random.randint(1, 5)
    await asyncio.sleep(load_time)
    message = f"Page {url} downloaded. Time spent: {load_time}s"
    print(message)
    return message


async def main(urls):
    """
    Execute asynchronous download tasks for a list of URLs and print results after all tasks complete.

    :param urls: A list of URLs to download.
    :type urls: list of str
    """
    # Create download tasks for each URL
    tasks = [download_page(link) for link in urls]
    # Await completion of all tasks and gather results
    results = await asyncio.gather(*tasks)

    # print("\nAll tasks have been completed.")
    # print("Results:")
    # for result in results:
    #     print(result)

# ---- URL List and Event Loop Execution ----

urls = [
    'https://www.google.com',
    'https://www.facebook.com',
    'https://www.instagram.com',
    'https://www.python.org',
    'https://www.yahoo.com'
]

# Run the main async function
asyncio.run(main(urls))
