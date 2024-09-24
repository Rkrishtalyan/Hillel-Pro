"""
Завдання 1: Built-in область видимості.

Демонстрація використання вбудованих функцій та їх перекриття локальними функціями.
1.	Написати функцію my_sum, яка перекриває вбудовану функцію sum. Функція поинна просто виводити повідомлення: 
    "This is my custom sum function!".
2.	Створити список чисел і викликати вбудовану функцію sum, щоб підсумувати значення списку.
3.	Викликати свою функцію my_sum, а потім ще раз спробувати скористатися вбудованою функцією sum.
"""

import builtins  # Для другого додаткового питання


def my_sum(*args):  # Без args у рядку 23 буде помилка "takes 0 positional arguments but 1 was given"
    """Override built-in sum() function."""
    global sum
    sum = my_sum
    print("This is my custom sum function!")


the_list = [1, 2, 3, 4]

print(sum(the_list))
my_sum()
print(sum(the_list))
# This is my custom sum function!  -  результат прінта із функції my_sum()
# None  -  у my_sum() не визначений return, тому вона за замовчуванням повертає 'None' у print


# Питання для закріплення:
# •	Що відбувається, коли локальна функція має те саме ім'я, що й вбудована?
# •	Як можна отримати доступ до вбудованої функції, навіть якщо вона перекрита?

# Відповідь на перше питання
print("\nAnswer to question 1")
print(sum)  # Змінна sum перевизначається і вказує тепер на нову функцію
print(sum(1, 2))

# Відповідь на друге питання
print("\nAnswer to question 2")
print(builtins.sum(the_list))
# Або створити ще одну змінну new_sum = sum ще на початку, поряд з the_list
# print(new_sum(the_list))
