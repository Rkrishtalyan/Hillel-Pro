"""
Завдання 3: Робота з CSV файлами.

Створи CSV-файл з даними про студентів, де кожен рядок містить: ім'я студента, вік, оцінку.

    Напиши програму, яка:
-   Читає дані з CSV-файлу.
-   Виводить середню оцінку студентів.
-   Додає нового студента до файлу.
"""

import csv


# ---- Вирішив трохи поімпровізувати ----
def create_csv_list(csv_file_name, headers_list, *lines):
    """
    Create a CSV file and write the given headers and lines to it.

    :param csv_file_name: The name of the CSV file to create.
    :type csv_file_name: str
    :param headers_list: A list of column headers for the CSV.
    :type headers_list: list
    :param lines: The data rows to be written into the CSV.
    :type lines: tuple of lists
    :return: The name of the created CSV file.
    :rtype: str
    """
    with open(csv_file_name, 'w', newline='') as csvfile:
        list_writer = csv.writer(csvfile, delimiter=',', quotechar=' ')
        list_writer.writerow(headers_list)
        for line in lines:
            list_writer.writerow(line)
    return csv_file_name


# ---- Creating a CSV file with student data ----
headers = ['Ім\'я', 'Вік', 'Оцінка']
student_1 = ['Петро', '21', '90']
student_2 = ['Марина', '22', '85']
student_3 = ['Андрій', '20', '88']

students_list = create_csv_list('hw_06_03_list.csv', headers, student_1, student_2, student_3)


# ---- Reading CSV file and calculating the average mark ----
with open(students_list, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    marks = []
    for row in reader:
        marks.append(int(row['Оцінка']))
    avg_mark = sum(marks) / len(marks)
    print(f"Average mark: {avg_mark:.2f}")


# ---- Adding a new student to the CSV file ----
student_4 = ['Даша', '19', '92']

with open(students_list, 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writerow(dict(zip(headers, student_4)))
    print(f"Student {student_4[0]} was added to the list")
