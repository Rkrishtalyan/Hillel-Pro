"""
9. Автоматичне резервне копіювання

Напишіть менеджер контексту, який буде створювати резервну копію важливого файлу перед його обробкою.
Якщо обробка пройде успішно, оригінальний файл замінюється новим.
У разі помилки резервна копія автоматично відновлюється.
"""

import os


class ReserveCopy:
    """
    Handle file backup and restoration using a context manager.

    This class creates a backup file when entering a context and restores the
    original file from the backup if an exception occurs during the context.

    :var file_name: Name of the original file to be backed up.
    :type file_name: str
    :var backup_file: Name of the backup file.
    :type backup_file: str
    """

    def __init__(self, file_name):
        """
        Initialize the ReserveCopy instance with the given file name.

        :param file_name: The name of the file to back up.
        :type file_name: str
        """
        self.file_name = file_name
        self.backup_file = file_name + '.bak'

    def __enter__(self):
        """
        Create a backup of the original file when entering the context.

        :return: The name of the original file.
        :rtype: str
        """
        with open(self.file_name, 'rb') as original_file:
            with open(self.backup_file, 'wb') as reserve_file:
                reserve_file.write(original_file.read())
        return self.file_name

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Restore the original file from the backup if an exception occurs.
        Delete the backup file on normal exit or after restoration.

        :param exc_type: Exception type, if any occurred.
        :type exc_type: type or None
        :param exc_value: Exception instance, if any occurred.
        :type exc_value: Exception or None
        :param traceback: Traceback object, if an exception occurred.
        :type traceback: traceback or None
        :return: False if an exception was handled, True otherwise.
        :rtype: bool
        """
        if exc_type is not None:
            with open(self.backup_file, 'rb') as backup_file:
                with open(self.file_name, 'wb') as original_file:
                    original_file.write(backup_file.read())
            os.remove(self.backup_file)
            print("Error occurred.  Restoring previous version of the file.")
            return False
        else:
            os.remove(self.backup_file)
            return True


# Testing the context manager
with ReserveCopy('hw_05_09_source.txt') as file_name:
    with open(file_name, 'a') as file:
        file.write(f'\nAdding the second line.')
    # raise Exception('Test exception')
