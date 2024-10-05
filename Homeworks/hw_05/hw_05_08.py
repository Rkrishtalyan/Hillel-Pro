"""
8. Конфігурація через контекстні менеджери.

Напишіть власний контекстний менеджер для роботи з файлом конфігурацій (формат .ini або .json).
Менеджер має автоматично зчитувати конфігурацію при вході в контекст і записувати зміни в файл після завершення роботи.
"""

import json


class JSONConfigManager:
    """
    Manage a JSON configuration file within a context manager.

    The JSONConfigManager class provides a convenient way to read and write
    JSON data using the 'with' statement.

    :var file_name: The name of the JSON file to manage.
    :type file_name: str
    :var content: The dictionary holding the content of the JSON file.
    :type content: dict
    """

    def __init__(self, file_name):
        """
        Initialize JSONConfigManager with the provided file name.

        :param file_name: The name of the JSON file to manage.
        :type file_name: str
        """
        self.file_name = file_name
        self.content = {}

    def __enter__(self):
        """
        Enter the runtime context related to this object.

        Reads the content of the JSON file and returns it as a dictionary.

        :return: The content of the JSON file as a dictionary.
        :rtype: dict
        """
        with open(self.file_name, 'r') as file:
            self.content = json.load(file)
        return self.content

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the runtime context related to this object.

        Writes the modified content back to the JSON file.

        :param exc_type: The exception type (if any).
        :param exc_value: The exception value (if any).
        :param traceback: The traceback object (if any).
        """
        with open(self.file_name, 'w') as file:
            json.dump(self.content, file, indent=4)


with JSONConfigManager('hw_05_08_config.json') as config:
    # {
    #     "database": {
    #         "host": "localhost",
    #         "port": 3306
    #     },
    #     "debug": true
    # }
    config["database"]["host"] = "db.example.com"
    config["debug"] = False
    config["logging"] = "verbose"
