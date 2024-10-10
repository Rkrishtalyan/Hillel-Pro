"""
Завдання 7. Тестування з використанням фікстур та тимчасових файлів.

Напишіть програму для роботи з файлами та протестуйте її,
використовуючи тимчасові файли та фікстури в pytest.

    Реалізуйте клас FileProcessor, який має такі методи:
-   write_to_file(file_path: str, data: str): записує дані у файл.
-   read_from_file(file_path: str) -> str: читає дані з файлу.

У тестах використовуйте фікстуру tmpdir для створення тимчасового файлу:
"""

import pytest


class FileProcessor:
    """
    Provide methods to write to and read from a file.

    This class allows appending data to a file and reading its contents.
    """

    @staticmethod
    def write_to_file(file_path, data):
        """
        Write data to a file.

        Appends the provided data to the file located at the specified file path.

        :param file_path: The path to the file where data will be written.
        :type file_path: str
        :param data: The data to be written to the file.
        :type data: str
        :return: None
        :rtype: None
        """
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(data)

    @staticmethod
    def read_from_file(file_path):
        """
        Read data from a file.

        Reads the content of the file at the specified file path
        and returns the data as a list of lines.

        :param file_path: The path to the file to be read.
        :type file_path: str
        :return: A list of lines from the file.
        :rtype: list
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.readlines()
            return data


# ---- Pytest Fixtures ----
@pytest.fixture
def file_processor() -> FileProcessor:
    """
    Provide a FileProcessor instance for testing.

    :return: An instance of FileProcessor.
    :rtype: FileProcessor
    """
    return FileProcessor()


# ---- Tests ----
def test_write_to_file(file_processor: FileProcessor, tmpdir) -> None:
    """
    Test that data can be written to a file.

    Creates a temporary file, writes data to it using FileProcessor,
    and asserts that the data matches the expected content.

    :param file_processor: An instance of FileProcessor for performing the test.
    :type file_processor: FileProcessor
    :param tmpdir: Pytest fixture providing a temporary directory for testing.
    :type tmpdir: LocalPath
    :return: None
    :rtype: None
    """
    temp_file = tmpdir.join("test_file.txt")
    file_processor.write_to_file(str(temp_file), "Hello there!")
    assert temp_file.read() == "Hello there!"


def test_read_from_file(file_processor: FileProcessor, tmpdir) -> None:
    """
    Test that data can be read from a file.

    Creates a temporary file, writes data to it, reads the data using FileProcessor,
    and asserts that the content matches the expected data.

    :param file_processor: An instance of FileProcessor for performing the test.
    :type file_processor: FileProcessor
    :param tmpdir: Pytest fixture providing a temporary directory for testing.
    :type tmpdir: LocalPath
    :return: None
    :rtype: None
    """
    temp_file = tmpdir.join("test_file.txt")
    temp_file.write("General Kenobi...\n")
    data = file_processor.read_from_file(str(temp_file))
    assert data == ["General Kenobi...\n"]
