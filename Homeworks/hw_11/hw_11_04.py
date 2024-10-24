"""
Завдання 4: Асинхронний таймаут.

Напишіть функцію slow_task(), яка імітує виконання завдання протягом 10 секунд.
Використовуючи asyncio.wait_for(), викличте slow_task() з таймаутом 5 секунд.
Якщо завдання не встигає виконатися за цей час,
виведіть повідомлення про перевищення часу очікування.
"""

import asyncio


# ---- Define slow task function ----
async def slow_task():
    """
    Execute a slow task by simulating a delay using asyncio.sleep.

    Prints a message before and after the delay to simulate task progress.
    """
    print("Alright! I will make it this time!")
    await asyncio.sleep(10)
    print('Yay!')


# ---- Main function and task timeout handling ----
async def main():
    """
    Execute the slow task with a timeout.

    Tries to complete the slow task within the timeout duration. If the task takes
    too long, it raises a TimeoutError and handles it by printing a failure message.
    """
    try:
        await asyncio.wait_for(slow_task(), timeout=5.0)
    except asyncio.TimeoutError:
        print('Too late, task! You failed again!')


# ---- Run the main function ----
asyncio.run(main())
