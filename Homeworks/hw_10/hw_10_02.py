"""
Задача 2: паралельна обробка зображень
Напишіть програму, яка обробляє кілька зображень одночасно (наприклад, змінює їх розмір
або застосовує фільтр).
Використовуйте модуль concurrent.futures і виконуйте обробку зображень у кількох процесах
або потоках.

Підказка: можна використовувати бібліотеку Pillow для обробки зображень.
"""

from concurrent.futures.thread import ThreadPoolExecutor
from PIL import Image
import time


# ---- Function to resize an image ----
def resize_image(file_path):
    """
    Resize the image to half of its original size and save it.

    :param file_path: The path to the image file.
    :type file_path: str
    """
    file_name = file_path.split('/')[-1]
    print(f"Getting image {file_name}...")
    time.sleep(0.5)

    # Open the image
    image = Image.open(file_path)

    # Calculate new size
    width, height = image.size
    new_size = (width // 2, height // 2)
    print(f"Original size: {width}x{height}")
    print(f"New size: {new_size[0]}x{new_size[1]}")

    # Resize and save the image
    resized_image = image.resize(new_size)
    resized_image.save(f"resized_{file_name}.jpg")
    print("Image saved!")


# ---- Main execution section ----
executor = ThreadPoolExecutor(max_workers=2)
image_1 = executor.submit(resize_image, '/Users/ruslank/PycharmProjects/Hillel_Pro/Tima/IMAG2418.jpg')
image_2 = executor.submit(resize_image, '/Users/ruslank/PycharmProjects/Hillel_Pro/Tima/IMAG2769.jpg')
image_3 = executor.submit(resize_image, '/Users/ruslank/PycharmProjects/Hillel_Pro/Tima/ZOE_0018_1.jpg')
