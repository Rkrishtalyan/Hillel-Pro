import builtins  # для другого додаткового питання


def my_sum(*args):  # без args у рядку 12 буде помилка "takes 0 positional arguments but 1 was given"
    global sum
    sum = my_sum
    print("This is my custom sum function!")


the_list = [1, 2, 3, 4]


print(sum(the_list))
my_sum()
print(sum(the_list))
# This is my custom sum function!  -  результат прінта із функції my_sum()
# None  -  у my_sum() не визначений return, тому вона за замовчуванням повертає 'None' у print


'''Additional question 1'''


def sum(a, b):
    return a + b


print("\nAnswer to question 1")
print(sum)  # змінна sum перевизначається і вказує тепер на нову функцію
print(sum(1, 2))


'''Additional question 2'''

print("\nAnswer to question 2")
print(builtins.sum(the_list))
# або створити ще одну змінну new_sum = sum ще на початку поряд з the_list
# print(new_sum(the_list))
