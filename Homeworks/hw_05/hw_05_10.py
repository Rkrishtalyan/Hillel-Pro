"""
10. Архівування та зберігання великих даних.

Реалізуйте менеджер контексту для архівування файлів (за допомогою модуля zipfile).
Менеджер автоматично створює архів, додає файли, а після виходу з блоку with – завершує архівування та закриває архів.
"""

import os
import zipfile


class ArchiveManager:
    """
    Manage the creation of a zip archive and handle file addition.

    This class supports the context manager protocol to create a zip
    archive and automatically add specified files to it.

    :var archive_name: The name of the archive to be created or appended to.
    :type archive_name: str
    :var files: The list of files to add to the archive.
    :type files: list
    """

    def __init__(self, archive_name, *files):
        """
        Initialize the ArchiveManager with the archive name and files to be added.

        :param archive_name: The name of the zip archive.
        :type archive_name: str
        :param files: The files to be added to the archive.
        :type files: list
        """
        self.archive_name = archive_name
        self.files = files
        self.archive = None

    def __enter__(self):
        """
        Enter the runtime context related to the archive creation.

        Opens the zip file in append mode and writes the provided files
        into the archive. Only the file names (without full catalog tree)
        are stored in the archive.

        :return: The zip file object.
        :rtype: zipfile.ZipFile
        """
        self.archive = zipfile.ZipFile(self.archive_name, 'a')
        existing_files = self.archive.namelist()
        for file in self.files:
            file_name_in_archive = os.path.basename(file)  # To add only files without full catalog tree
            if file_name_in_archive in existing_files:
                print(f"Skipping {file_name_in_archive}: already exists in the archive.")
            else:
                self.archive.write(file, arcname=file_name_in_archive)
                print(f"File {file_name_in_archive} was added to the archive")
        return self.archive

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context and close the archive.

        Ensures that the zip archive is closed when the context manager exits.
        """
        self.archive.close()


# Creating a list of full files paths:
directory = '/Users/ruslank/PycharmProjects/Hillel_Pro/Tima'
files = [os.path.join(directory, file) for file in os.listdir(directory)]

# Testing the auto-archive context
with ArchiveManager("hw_05_10_archive.zip", *files) as archive:
    pass
