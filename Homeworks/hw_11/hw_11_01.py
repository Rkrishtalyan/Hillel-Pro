"""
Завдання 1: Основи асинхронності.

Напишіть асинхронну функцію download_page(url: str), яка симулює завантаження сторінки за допомогою asyncio.sleep().
Функція повинна приймати URL та "завантажувати" сторінку за випадковий проміжок часу від 1 до 5 секунд.
Після завершення завантаження, функція повинна вивести повідомлення з URL і часом завантаження.
Напишіть асинхронну функцію main(urls: list), яка приймає список з декількох URL
і завантажує їх одночасно, використовуючи await для паралельного виконання функції download_page().
"""

import asyncio
import random


# ---- Function Definitions ----

async def download_page(url):
    """
    Simulate downloading a page from the given URL.

    This function simulates downloading a page by pausing for a random time
    between 1 and 5 seconds, printing the message when the download is complete.

    :param url: The URL of the page to download.
    :type url: str
    :return: A message indicating the download completion and time spent.
    :rtype: str
    """
    print(f"Retrieving page from {url}")
    load_time = random.randint(1, 5)
    await asyncio.sleep(load_time)
    message = f"Page {url} downloaded. Time spent: {load_time}s"
    print(message)
    return message


async def main():
    """
    Execute asynchronous downloading of multiple web pages.

    This function gathers tasks to download pages asynchronously and
    waits for all tasks to complete. It prints the results of each download.

    :return: None
    """
    urls = [
        'https://www.google.com',
        'https://www.facebook.com',
        'https://www.instagram.com',
        'https://www.python.org',
        'https://www.yahoo.com'
    ]

    tasks = [download_page(link) for link in urls]
    results = await asyncio.gather(*tasks)

    print("\nAll tasks have been completed.")
    print("Results:")
    for result in results:
        print(result)


# ---- Program Execution ----
if __name__ == "__main__":
    asyncio.run(main())
