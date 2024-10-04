"""
2. Ітератор для генерації унікальних ідентифікаторів

Створіть ітератор, який генерує унікальні ідентифікатори (наприклад, на основі UUID або хеш-функції).
Ідентифікатори повинні генеруватися один за одним при кожній ітерації, і бути унікальними.
"""

import uuid


class GuidGenerator:
    """
    Represent a generator for UUIDs (Universally Unique Identifiers).

    This class implements the iterator protocol to generate UUIDs
    using the built-in `uuid` module.
    """

    def __iter__(self):
        """
        Return the iterator object (self) to allow iteration.

        :return: self (iterator object)
        :rtype: GuidGenerator
        """
        return self

    def __next__(self):
        """
        Generate and return the next UUID.

        This method generates a new version 4 UUID each time it's called.

        :return: A new UUID
        :rtype: uuid.UUID
        """
        return uuid.uuid4()


for i, guid in enumerate(GuidGenerator()):
    print(guid)
    if i >= 9:  # Пример остановки после 10 UUID
        break
