"""
3. Збір статистики про зображення

У вас є каталог з великою кількістю зображень. Напишіть ітератор, який по черзі відкриває кожне зображення
(наприклад, за допомогою модуля PIL), витягує з нього метадані (розмір, формат тощо) і зберігає ці дані у файл CSV.
"""

import os
import csv
from PIL import Image


class ImageAnalyzer:
    """
    Analyze images in a directory and write metadata to a CSV file.

    This class iterates over image files in a directory, retrieves their format,
    dimensions, and writes this data to a CSV file.

    :param directory: The directory where the image files are located.
    :type directory: str
    :param csv_filename: The filename of the CSV where the metadata will be written.
    :type csv_filename: str
    """

    def __init__(self, directory, csv_filename):
        """
        Initialize the ImageAnalyzer instance.

        :param directory: The directory to search for image files.
        :type directory: str
        :param csv_filename: The name of the CSV file to write image metadata.
        :type csv_filename: str
        """
        self.directory = directory
        self.csv_filename = csv_filename
        self.files = os.listdir(directory)
        self.index = 0
        self.csvfile = open(self.csv_filename, 'w', newline='', encoding='utf-8')
        self.fieldnames = ['Filename', 'Format', 'Width', 'Height']
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def __iter__(self):
        """
        Return the iterator object itself.

        :return: The ImageAnalyzer instance.
        :rtype: ImageAnalyzer
        """
        return self

    def __next__(self):
        """
        Iterate through the image files in the directory and write their metadata to the CSV file.

        :return: A dictionary containing the filename, format, width, and height of the image.
        :rtype: dict
        :raises StopIteration: When no more image files are left to process.
        """
        while self.index < len(self.files):
            filename = self.files[self.index]
            self.index += 1
            filepath = os.path.join(self.directory, filename)

            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                try:
                    with Image.open(filepath) as img:
                        info = {
                            'Filename': filename,
                            'Format': img.format,
                            'Width': img.width,
                            'Height': img.height
                        }
                        self.writer.writerow(info)
                        return info
                except IOError:
                    print(f"Не вдалося відкрити зображення {filename}.")
                    continue
            else:
                continue

        self.csvfile.close()
        raise StopIteration


image_directory = '/Users/ruslank/PycharmProjects/Hillel_Pro/Tima'
csv_file = 'hw_05_03.csv'

for metadata in ImageAnalyzer(image_directory, csv_file):
    print(metadata)  # згенерований csv лежить у Гіті
