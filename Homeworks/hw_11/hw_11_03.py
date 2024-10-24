"""
Завдання 3: Асинхронні черги.

Реалізуйте асинхронну чергу завдань за допомогою asyncio.Queue.
Створіть функцію producer(queue), яка додає 5 завдань до черги із затримкою в 1 секунду.
Напишіть функцію consumer(queue), яка забирає завдання з черги, виконує його
(наприклад, виводить повідомлення), імітуючи роботу з кожним завданням із затримкою в 2 секунди.
Створіть функцію main(), яка одночасно запускає і producer, і кілька споживачів (consumer)
за допомогою asyncio.gather(), щоб споживачі обробляли завдання в міру їх появи в черзі.
"""

import asyncio
import threading

consumer_counter = 1
counter_lock = threading.Lock()


# ---- Producer Task Definition ----
async def producer(queue):
    """
    Produce tasks and put them in the queue.

    The producer creates tasks with names 'task_1' to 'task_5',
    simulates task creation with a 1-second delay between each task,
    and places them in the queue.

    :param queue: An asyncio queue to hold the tasks.
    :type queue: asyncio.Queue
    """
    print("Producer started")
    for i in range(1, 6):
        task = f"task_{i}"
        await asyncio.sleep(1)
        await queue.put(task)
        print(f"Producer: {task} created.")
    print("Producer has finished producing tasks.")


# ---- Consumer Task Definition ----
async def consumer(queue):
    """
    Consume tasks from the queue and process them.

    Each consumer retrieves tasks from the queue, processes them (simulates with a 2-second delay),
    and marks them as done.

    :param queue: An asyncio queue containing tasks to be processed.
    :type queue: asyncio.Queue
    """
    global consumer_counter
    with counter_lock:
        consumer_name = f"Consumer_{consumer_counter}"
        consumer_counter += 1
    print(f"{consumer_name} initiated...")

    while True:
        task = await queue.get()
        try:
            print(f"{consumer_name} found and processing: {task}")
            await asyncio.sleep(2)
            print(f"{consumer_name} completed: {task}")
        finally:
            queue.task_done()


# ---- Main Coroutine ----
async def main():
    """
    Manage the execution of the producer and consumers.

    Creates a producer and multiple consumers,
    waits for the producer to finish and the queue to be processed,
    and then cancels the consumer tasks once all tasks are done.

    :return: None
    """
    queue = asyncio.Queue()
    num_consumers = 3

    producer_task = asyncio.create_task(producer(queue))
    consumer_tasks = [asyncio.create_task(consumer(queue)) for _ in range(num_consumers)]

    await producer_task
    await queue.join()

    # Cancel consumer tasks since there are no more tasks
    for c in consumer_tasks:
        c.cancel()

    await asyncio.gather(*consumer_tasks, return_exceptions=True)

    print("All tasks have been processed and consumers have been cancelled.")


# ---- Program Entry Point ----
if __name__ == "__main__":
    asyncio.run(main())
