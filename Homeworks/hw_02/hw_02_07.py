"""
Завдання 7: Трекер витрат.

Розробити програму для трекінгу витрат, яка використовує глобальні змінні
для зберігання загальної суми витрат.

1.  Створити глобальну змінну total_expense і функцію add_expense,
    яка приймає суму витрат і додає її до загальної суми.
2.  Додати функцію get_expense, яка повертає загальну суму витрат.
3.  Створити інтерфейс (консольний), щоб користувач міг додавати витрати
    і переглядати загальну суму.
"""

# ---- Initialize total expense ----
total_expense = 0


# ---- Define expense management functions ----
def add_expense(value):
    """
    Add an expense to the total expense tracker.

    This function increments the global `total_expense` by the provided value.

    :param value: Expense amount to add.
    :type value: int
    """
    global total_expense
    total_expense += value


def get_expense():
    """
    Display the total expense.

    Prints the cumulative value of all added expenses.
    """
    print(f"Загальна сума витрат: {total_expense}")


# ---- Main program interface ----
print("Вітаємо у Вашому особистому менеджері витрат!")
print("\nВи можете обрати одну з дій:")
print("+ - додати суму витрат;")
print("= - подивитись загальну суму витрат;")
print("інший ключ - завершення програми.")

while True:
    action = input("\nОберіть бажану дію: ")
    if action == "+":
        expense = int(input("Введіть суму витрат: "))
        add_expense(expense)
    elif action == "=":
        get_expense()
    else:
        break

print("\nДякуємо що скористалися нашою програмою. Гарного дня!")

# Можна було просто виводити поточну суму витрат після кожного додавання,
# але вирішив додати інтерактивності.
