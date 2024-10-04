"""
4. Генератор для обробки великих файлів.

Реалізуйте генератор, який читає великий текстовий файл рядок за рядком (наприклад, лог-файл)
і повертає лише ті рядки, що містять певне ключове слово.
Використайте цей генератор для фільтрації файлу та запису відповідних рядків у новий файл.
"""


def log_tracer(file_name, keyword):
    """
    Trace lines in a file that contain a specific keyword.

    :param file_name: The name of the file to be read.
    :type file_name: str
    :param keyword: The keyword to search for in the file.
    :type keyword: str
    :yield: Lines containing the keyword.
    :rtype: generator
    """
    with open(file_name, 'r') as read_file:
        for line in read_file:
            if keyword in line:
                yield line


chronicles = log_tracer("hw_05_04.txt", "Emperor")
with open("hw_05_04_emperor.txt", 'w') as write_file:
    while True:
        try:
            write_file.write(next(chronicles))
        except StopIteration:
            break
