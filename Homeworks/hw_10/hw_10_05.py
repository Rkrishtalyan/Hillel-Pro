"""
Задача 5: паралельний пошук у файлах
Реалізуйте програму, яка шукає певний текст у кількох великих файлах одночасно,
використовуючи потоки або процеси. Для кожного файлу створіть окремий потік або процес.
"""

import threading


# ---- Function Definition Section ----
def log_tracer(file_path, keyword):
    """
    Trace and print the lines of a log file that contain a specified keyword.

    :param file_path: The path to the log file.
    :type file_path: str
    :param keyword: The keyword to search for in the log file.
    :type keyword: str
    """
    file_name = file_path.split('/')[-1]

    with open(file_path, 'r') as read_file:
        line_counter = 1
        for line in read_file:
            if keyword in line:
                print(
                    f'Keyword "{keyword}" was found on line {line_counter} of file {file_name}')
            line_counter += 1


# ---- Thread Creation and Execution Section ----
task_1 = threading.Thread(
    target=log_tracer,
    args=(
        '/Users/ruslank/PycharmProjects/Hillel_Pro/Homeworks/hw_10/hw_10_05_logs/morrowind_log.txt',
        'Sheogorath'
    )
)
task_2 = threading.Thread(
    target=log_tracer,
    args=(
        '/Users/ruslank/PycharmProjects/Hillel_Pro/Homeworks/hw_10/hw_10_05_logs/oblivion_log.txt',
        'Sheogorath'
    )
)
task_3 = threading.Thread(
    target=log_tracer,
    args=(
        '/Users/ruslank/PycharmProjects/Hillel_Pro/Homeworks/hw_10/hw_10_05_logs/skyrim_log.txt',
        'Sheogorath'
    )
)

task_1.start()
task_2.start()
task_3.start()

task_1.join()
task_2.join()
task_3.join()
