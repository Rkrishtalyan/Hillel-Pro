"""
6. Ітерація через файли в каталозі.

Напишіть ітератор, який буде повертати всі файли в заданому каталозі по черзі.
Для кожного файлу виведіть його назву та розмір.
"""

import os


class CatalogIterator:
    """
    Iterate over files in a directory and provide file details.

    The CatalogIterator class provides an interface to iterate through the files
    in a specified directory and print their sizes.

    :var directory: The directory to iterate over.
    :type directory: str
    :var files: List of files in the specified directory.
    :type files: list
    :var index: The current position in the iteration.
    :type index: int
    """

    def __init__(self, directory):
        """
        Initialize a CatalogIterator instance with a directory.

        :param directory: The directory to iterate over.
        :type directory: str
        """
        self.directory = directory
        self.files = os.listdir(directory)
        self.index = 0

    def __iter__(self):
        """
        Return the iterator object itself.

        :return: The CatalogIterator instance.
        :rtype: CatalogIterator
        """
        return self

    def __next__(self):
        """
        Return the next file in the directory.

        Raises StopIteration when all files have been iterated.

        :return: The name of the next file.
        :rtype: str
        :raises StopIteration: When no more files are available.
        """
        if self.index >= len(self.files):
            raise StopIteration

        file_name = self.files[self.index]
        self.index += 1
        file_path = os.path.join(self.directory, file_name)
        file_size = os.path.getsize(file_path)

        # Format and print file size
        self._print_file_size(file_name, file_size)

        return file_name

    def _print_file_size(self, file_name, file_size):
        """
        Print the file size in human-readable format (bytes, KB, MB).

        :param file_name: The name of the file.
        :type file_name: str
        :param file_size: The size of the file in bytes.
        :type file_size: int
        """
        if file_size >= 1024 * 1024:
            size_str = f"{file_size / 1024 / 1024:.2f} MBs"
        elif file_size >= 1024:
            size_str = f"{file_size / 1024:.2f} KBs"
        else:
            size_str = f"{file_size:.2f} bytes"

        print(f"File: {file_name}, size: {size_str}")


# Example usage
image_directory = '/Users/ruslank/PycharmProjects/Hillel_Pro/Tima'
cycle_iteration = CatalogIterator(image_directory)
manual_iteration = CatalogIterator(image_directory)

# Iterating with cycle
print("Cycle iteration:")
for file in cycle_iteration:
    pass

# Iterating manually with next()
print()
print("Manual iteration:")
next(manual_iteration)
next(manual_iteration)
next(manual_iteration)
try:
    next(manual_iteration)
except StopIteration:
    pass
