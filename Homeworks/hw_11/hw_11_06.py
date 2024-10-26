"""
Завдання 6: Завантаження зображень з декількох сайтів.

Уявімо, що ми розробляємо веб-скрапер, який має завантажити зображення з декількох сайтів одночасно.
Кожне завантаження зображення - це окрема операція введення-виводу, яка може зайняти певний час.

Створити асинхронну функцію download_image, яка приймає URL зображення та ім'я файлу для збереження.
Вона використовуватиме aiohttp для виконання HTTP-запиту та збереження отриманих даних у файл.

Головна асинхронна функція main створює список завдань (tasks),
кожне з яких відповідає за завантаження одного зображення.
Функція asyncio.gather дозволяє запускати всі завдання одночасно і очікувати їх завершення.
"""

import asyncio
import aiohttp
import aiofiles


# ---- Define asynchronous image download function ----
async def download_image(session, url, file_name):
    """
    Download an image from the specified URL and save it to a file.

    :param session: The aiohttp ClientSession used for making HTTP requests.
    :type session: aiohttp.ClientSession
    :param url: The URL of the image to download.
    :type url: str
    :param file_name: The name of the file to save the downloaded image.
    :type file_name: str
    """
    async with session.get(url) as resp:
        if resp.status == 200:
            async with aiofiles.open(file_name, 'wb') as f:
                await f.write(await resp.read())
        else:
            print(f"Failed to download {url} with status {resp.status}")


# ---- Define main asynchronous function to handle multiple downloads ----
async def main(urls):
    """
    Download multiple images concurrently from a list of URLs.

    :param urls: List of image URLs to download.
    :type urls: list[str]
    """
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            file_name = url.split('/')[-1]
            tasks.append(download_image(session, url, file_name))
        await asyncio.gather(*tasks)


# ---- Define list of image URLs and execute main function ----
urls = [
    'https://upload.wikimedia.org/wikipedia/commons/a/a8/Tour_Eiffel_Wikimedia_Commons.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg',
    'https://upload.wikimedia.org/wikipedia/commons/b/b2/Sugarloaf_Sunrise_2.jpg'
]

asyncio.run(main(urls))
