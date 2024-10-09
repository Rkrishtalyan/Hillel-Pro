"""
Завдання 1. Модульне тестування з використанням unittest.

Напишіть простий застосунок для обробки рядків та напишіть модульні тести
з використанням бібліотеки unittest. Створіть клас StringProcessor з методами:

-   reverse_string(s: str) -> str: повертає перевернутий рядок.
-   capitalize_string(s: str) -> str: робить першу літеру рядка великої.
-   count_vowels(s: str) -> int: повертає кількість голосних у рядку.

Напишіть тести для кожного методу, перевіряючи кілька різних сценаріїв:

-   порожні рядки.
-   рядки з різними регістрами.
-   рядки з цифрами та символами.

Використовуйте декоратор @unittest.skip для пропуску тесту, який тестує метод
reverse_string з порожнім рядком, оскільки це відома проблема, яку ви плануєте вирішити пізніше.
"""

import unittest


class StringProcessor:
    """
    Provide static methods to process strings, such as reversing, capitalizing,
    and counting vowels.
    """

    @staticmethod
    def reverse_string(s):
        """
        Reverse the given string.

        :param s: The string to reverse.
        :type s: str
        :return: The reversed string.
        :rtype: str
        """
        return s[::-1]

    @staticmethod
    def capitalize_string(s):
        """
        Capitalize the first letter of the given string.

        :param s: The string to capitalize.
        :type s: str
        :return: The capitalized string.
        :rtype: str
        """
        return s.capitalize()

    @staticmethod
    def count_vowels(s):
        """
        Count the number of vowels in the given string. Supports English and Ukrainian vowels.

        :param s: The string in which vowels are counted.
        :type s: str
        :return: The number of vowels.
        :rtype: int
        """
        vowels = 'aeiouAEIOUаеиіоуюяєїАЕИІОУЮЯЄЇ'
        return sum(1 for char in s if char in vowels)


class TestClassProcessor(unittest.TestCase):
    """
    Unit tests for the StringProcessor class.
    """

    def setUp(self):
        """
        Set up an instance of StringProcessor for testing.
        """
        self.text = StringProcessor()

    @unittest.skip("Known issue, will be fixed later.")
    def test_reverse_string_empty(self):
        """
        Test reversing an empty string.
        """
        self.assertEqual(self.text.reverse_string(""), "")

    def test_reverse_string(self):
        """
        Test reversing various non-empty strings.
        """
        self.assertEqual(self.text.reverse_string("Hello there!"), "!ereht olleH")
        self.assertEqual(self.text.reverse_string("GeNeRaL KeNoBi..."), "...iBoNeK LaReNeG")
        self.assertEqual(self.text.reverse_string("R2-D2 Beep-b@@p @#$%"), "%$#@ p@@b-peeB 2D-2R")

    def test_capitalize_string(self):
        """
        Test capitalizing various strings.
        """
        self.assertEqual(self.text.capitalize_string("hello there!"), "Hello there!")
        self.assertEqual(self.text.capitalize_string("genERaL KeNoBI..."), "General kenobi...")
        self.assertEqual(self.text.capitalize_string("123abc"), "123abc")
        self.assertEqual(self.text.capitalize_string(""), "")

    def test_count_vowels(self):
        """
        Test counting vowels in various strings.
        """
        self.assertEqual(self.text.count_vowels("Hello there!"), 4)
        self.assertEqual(self.text.count_vowels("General Kenobi..."), 6)
        self.assertEqual(self.text.count_vowels("R2-D2"), 0)
        self.assertEqual(self.text.count_vowels("123aeiouAEIOU"), 10)
        self.assertEqual(self.text.count_vowels(""), 0)


# ---- Run tests ----
if __name__ == "__main__":
    unittest.main()
