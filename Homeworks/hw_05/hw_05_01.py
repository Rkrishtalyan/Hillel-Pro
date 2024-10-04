"""
1. Створення власного ітератора для зворотного читання файлу.

Напишіть власний ітератор, який буде зчитувати файл у зворотному порядку — рядок за рядком з кінця файлу до початку.
Це може бути корисно для аналізу лог-файлів, коли останні записи найважливіші.
"""


class ReverseLineReader:
    """
    Iterate over lines in a file in reverse order.

    The ReverseLineReader class reads all lines from a given file
    and provides an iterator to access them in reverse order.

    :var lines: The lines of the file.
    :type lines: list[str]
    :var position: The current position in the list of lines.
    :type position: int
    """

    def __init__(self, file_path):
        """
        Initialize the ReverseLineReader with the file's path.

        Reads the file's content and stores it in a list of lines.

        :param file_path: The path to the file to be read.
        :type file_path: str
        """
        with open(file_path, 'r') as file:
            self.lines = file.readlines()
        self.position = len(self.lines)

    def __iter__(self):
        """
        Return the iterator object itself.

        :return: The iterator object.
        :rtype: ReverseLineReader
        """
        return self

    def __next__(self):
        """
        Return the next line from the file in reverse order.

        :return: The next line from the file, stripped of leading/trailing whitespace.
        :rtype: str
        :raises StopIteration: When there are no more lines to return.
        """
        if self.position == 0:
            raise StopIteration
        self.position -= 1
        return self.lines[self.position].strip()


reverse_log = ReverseLineReader("hw_05_01.txt")
for line in reverse_log:
    print(line)
