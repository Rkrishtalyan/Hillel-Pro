"""Завдання 6: Калькулятор з використанням замикань

Створити калькулятор, який використовує замикання для створення функцій додавання, віднімання, множення та ділення.

1.	Написати функцію create_calculator, яка приймає оператор (наприклад, '+', '-', '*', '/')
    та повертає функцію для виконання обчислень.
2.	Використати цю функцію, щоб створити калькулятор для кількох операцій, і протестувати його.
"""


def create_calculator(operator):
    """
    Create and return calculation function based on provided operator.

    Supports +, -, *, / operators only.
    """
    def adding(a, b):
        """Summarize two values."""
        return a + b

    def subtracting(a, b):
        """Subtract one value from another."""
        return a - b

    def multiplying(a, b):
        """Multiply one value by another."""
        return a * b

    def dividing(a, b):
        """Divide one value by another. Return "Division by zero" if divisor = 0."""
        if b != 0:
            return a / b
        else:
            return "Division by zero"

    if operator == "+":
        return adding
    elif operator == "-":
        return subtracting
    elif operator == "*":
        return multiplying
    elif operator == "/":
        return dividing


action = "+"
addition = create_calculator(action)
print(addition(5,3))
print(addition(10, 5))

action = "-"
subtraction = create_calculator(action)
print(subtraction(5, 3))
print(subtraction(10, 5))

action = "+"
multiplication = create_calculator(action)
print(multiplication(5,3))
print(multiplication(10, 5))

action = "/"
multiplication = create_calculator(action)
print(multiplication(5,3))
print(multiplication(10, 0))

action = input("Enter operator manually: ")
calculate = create_calculator(action)
x = int(input("Enter first value: "))
y = int(input("enter second value: "))
print(f"Result: {calculate(x, y)}")
