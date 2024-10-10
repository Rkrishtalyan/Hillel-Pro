"""
Завдання 9. Тестування різних сценаріїв скіпів та умов (опціонально).

Завдання: Напишіть програму для перевірки віку користувачів
та додайте різні скіпи та умови у тестах.

Реалізуйте клас AgeVerifier, який перевіряє вік:
is_adult(age: int) -> bool: повертає True, якщо вік більше або дорівнює 18.

    Напишіть тести, які:
-   перевіряють коректну роботу функції для різного віку,
-   пропускають тест, якщо вік менший за 0 (некоректне значення),
    з використанням pytest.mark.skip.

Додайте умовний скіп, який пропустить тест, якщо вік більше 120,
тому що це малоймовірний сценарій.
"""

import unittest
import pytest


# ---- Class Definitions ----
class AgeVerifier:
    """
    Provide functionality to verify if the given age qualifies as adult.

    The AgeVerifier class contains static methods to check age criteria.
    """

    @staticmethod
    def is_adult(age):
        """
        Check if the provided age qualifies as an adult.

        :param age: The age to be verified.
        :type age: int
        :return: True if the age is 18 or older, False otherwise.
        :rtype: bool
        """
        if age >= 18:
            return True
        return False


class TestAgeVerifier(unittest.TestCase):
    """
    Test the AgeVerifier class methods using unittest framework.
    """

    def setUp(self):
        """
        Set up AgeVerifier instance for testing.
        """
        self.age = AgeVerifier()

    def test_is_adult_ut(self):
        """
        Test is_adult method with various ages using unittest assertions.
        """
        self.assertEqual(self.age.is_adult(20), True)
        self.assertEqual(self.age.is_adult(65), True)
        self.assertEqual(self.age.is_adult(10), False)

    @unittest.skip("Age is less than 0.")
    def test_is_adult_ut_below_zero(self):
        """
        Test is_adult method when age is less than zero.
        """
        self.assertEqual(self.age.is_adult(-5), False)


# ---- Pytest Test Functions ----
@pytest.mark.parametrize('age, output', [
    (25, True),
    (99, True),
    (3, False)
])
def test_is_adult_pt(age, output):
    """
    Test is_adult method with various ages using pytest parametrize.

    :param age: Age to test.
    :param output: Expected result of is_adult function.
    """
    assert AgeVerifier.is_adult(age) == output


@pytest.mark.skip(reason="Age is less than 0")
def test_is_adult_pt_below_zero():
    """
    Skip test when age is less than 0.
    """
    assert AgeVerifier.is_adult(-5)


@pytest.mark.parametrize('age', [120, 121, 130])
def test_is_adult_pt_conditional(age):
    """
    Test is_adult method with conditional pytest.skip logic for age values over 120.

    :param age: Age to test.
    """
    if age > 120:
        pytest.skip("Неправильне значення віку")
    assert AgeVerifier.is_adult(age) == (age >= 18)


age = 121  # це єдиний спосіб як я зміг виконати умову скіпу нижче саме у такій формі як записано


@pytest.mark.skipif(age > 120, reason="Неправильне значення віку")
def test_is_adult_pt_skip_if():
    """
    Skip test based on a conditional age value with pytest.skipif.
    """
    assert AgeVerifier.is_adult(age) is True


# ---- Program Execution ----
if __name__ == '__main__':
    unittest.main()
