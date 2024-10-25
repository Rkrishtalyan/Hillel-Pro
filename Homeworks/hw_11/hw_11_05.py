"""
Завдання 5: Створення простого асинхронного веб-сервера.

1.  Використовуючи бібліотеку aiohttp, створіть простий асинхронний веб-сервер, який має два маршрути:

-   /, який повертає простий текст "Hello, World!".
-   /slow, який симулює довгу операцію з затримкою в 5 секунд і повертає текст "Operation completed".

2.  Запустіть сервер і перевірте, що він може обробляти кілька запитів одночасно
(зокрема, маршрут /slow не блокує інші запити).
"""

import asyncio
from aiohttp import web


# ---- Request Handlers ----

async def handle_root(request):
    """
    Handle the root endpoint by returning a simple greeting.

    :param request: The incoming HTTP request.
    :type request: aiohttp.web.Request
    :return: A greeting response.
    :rtype: aiohttp.web.Response
    """
    return web.Response(text="Hello, World!")


async def handle_slow(request):
    """
    Handle the slow endpoint with a delay to simulate a long operation.

    :param request: The incoming HTTP request.
    :type request: aiohttp.web.Request
    :return: A response indicating operation completion after a delay.
    :rtype: aiohttp.web.Response
    """
    await asyncio.sleep(5)
    return web.Response(text="Operation completed")


# ---- Application Setup ----

app = web.Application()
app.add_routes([
    web.get('/', handle_root),
    web.get('/slow', handle_slow),
])

# ---- Run Application ----

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8080)
