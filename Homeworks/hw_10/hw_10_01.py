"""
Задача 1: завантаження файлів із мережі
Створіть програму, яка завантажує кілька файлів із мережі одночасно за допомогою потоків.
Ваша програма повинна використовувати модуль threading для створення декількох потоків,
кожен з яких відповідає за завантаження окремого файлу.

Підказка: використайте бібліотеки requests або urllib для завантаження файлів.
"""

# ---- Imports ----
import threading
import requests

# ---- Global Variables ----
file_counter = 1
counter_lock = threading.Lock()


# ---- Functions ----
def get_image(url):
    """
    Download an image from a given URL and save it locally.

    The function retrieves an image from the provided URL, increments the global
    file_counter under thread safety, and saves the image as a JPEG file.

    :param url: The URL of the image to be downloaded.
    :type url: str
    """
    global file_counter

    print("Retrieving image...")
    response = requests.get(url, timeout=30)

    with counter_lock:
        file_name = f'image_{file_counter}.jpg'
        file_counter += 1

    with open(file_name, 'wb') as file:
        file.write(response.content)

    print(f"Image {file_name} downloaded successfully!")


# ---- Main Execution ----
url_1 = 'https://drive.google.com/uc?export=download&id=1eYpHEg8Kj7eVsftzqBLmBEoGfHrb2_aI'
url_2 = 'https://drive.google.com/uc?export=download&id=13P4v6vGaGhpNI8FM1EV4YTPS_52Fm99l'

task_1 = threading.Thread(target=get_image, args=(url_1,))
task_2 = threading.Thread(target=get_image, args=(url_2,))

task_1.start()
task_2.start()

task_1.join()
task_2.join()
