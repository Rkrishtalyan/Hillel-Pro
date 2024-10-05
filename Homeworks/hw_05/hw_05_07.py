"""
7. Парсинг великих лог-файлів для аналітики.

Уявіть, що у вас є великий лог-файл від веб-сервера.
Створіть генератор, який зчитує файл порціями (по рядку) і повертає тільки рядки з помилками (код статусу 4XX або 5XX).
Запишіть ці помилки в окремий файл для подальшого аналізу.
"""


def log_parser_4xx_5xx(file_name):
    """
    Parse the log file and yield lines containing 4xx or 5xx status codes.

    This function opens a log file and iterates over each line. It splits each line into parts
    and checks if any part is a three-digit status code that starts with '4' or '5'.
    If found, it yields the entire line.

    :param file_name: The path to the log file.
    :type file_name: str
    :yield: Lines that contain 4xx or 5xx status codes.
    :rtype: generator
    """
    with open(file_name, 'r') as read_file:
        for line in read_file:
            parts = line.split()
            for part in parts:
                if part.isdigit() and len(part) == 3:
                    if part.startswith('4') or part.startswith('5'):
                        yield line
                        break
    # Якщо точно знати формат запису у лог-файлі, то можна покращити логіку, перевіряючи конкретну позицію.
    # Наприклад, якщо помилка друга з кінця, то можна перевіряти саме parts[-2].
    # Тут зробив більш загальний парсер, тому є помилкові входження у аутпуті.


def log_parser_custom(file_name, *args):
    """
    Parse the log file and yield lines containing any custom arguments.

    This function opens a log file and iterates over each line. If any of the
    custom arguments provided in *args are present in a line, the line is yielded.

    :param file_name: The path to the log file.
    :type file_name: str
    :param args: Custom arguments to search for in the log file.
    :type args: str
    :yield: Lines that contain any of the custom arguments.
    :rtype: generator
    """
    with open(file_name, 'r') as read_file:
        for line in read_file:
            if any(arg in line for arg in args):
                yield line


# Testing log parser for all 4xx and 5xx error codes
errors_4xx_5xx_log = log_parser_4xx_5xx("hw_05_07_source.txt")
with open("hw_05_07_output_all.txt", 'w') as write_file:
    while True:
        try:
            write_file.write(next(errors_4xx_5xx_log))
        except StopIteration:
            break


# Testing log parser with custom error code entry
error_404_log = log_parser_custom("hw_05_07_source.txt", "404")
with open("hw_05_07_output_custom.txt", 'w') as write_file:
    while True:
        try:
            write_file.write(next(error_404_log))
        except StopIteration:
            break
