"""
Завдання 2: Робота з асинхронними HTTP-запитами.

Використовуючи бібліотеку aiohttp, створіть асинхронну функцію fetch_content(url: str),
яка виконує HTTP-запит до вказаного URL і повертає вміст сторінки.
Створіть асинхронну функцію fetch_all(urls: list), яка приймає список URL
і завантажує вміст усіх сторінок паралельно.
Використайте await та об'єднання кількох завдань (asyncio.gather()),
щоб завантаження всіх сторінок виконувалося одночасно.
Обробіть можливі помилки запитів, щоб у разі проблеми з підключенням
функція повертала відповідне повідомлення про помилку.
"""

import asyncio
import aiohttp


async def fetch_content(session, url):
    """
    Fetch content from the given URL using the provided session.

    :param session: The aiohttp ClientSession object to make requests.
    :type session: aiohttp.ClientSession
    :param url: The URL to fetch content from.
    :type url: str
    :return: The content of the URL as a string.
    :rtype: str
    :raises: Raises an exception if the request fails.
    """
    async with session.get(url) as response:
        response.raise_for_status()  # raises exception for 4xx and 5xx errors
        return await response.text()


async def fetch_all(urls):
    """
    Fetch content from a list of URLs asynchronously.

    :param urls: A list of URLs to fetch content from.
    :type urls: list of str
    :return: A list of results, which may include exceptions if fetching failed.
    :rtype: list
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(fetch_content(session, url))
            tasks.append(task)
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results


# ---- Main Program Execution ----
urls = [
    "https://www.example.com",
    "https://www.python.org",
    "https://nonexistent.url"
]

# Execute the asynchronous fetch_all function
results = asyncio.run(fetch_all(urls))

# ---- Print the results ----
for index, result in enumerate(results):
    url = urls[index]
    print(f"URL: {url}")
    if isinstance(result, Exception):
        print(f"Error fetching {url}: {result}\n")
    else:
        result = result[:100] + "..." if len(result) > 100 else result
        print(f"Result:\n{result}\n")
