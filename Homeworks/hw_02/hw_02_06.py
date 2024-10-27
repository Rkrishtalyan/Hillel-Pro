"""Завдання 6: Калькулятор з використанням замикань.

Створити калькулятор, який використовує замикання для створення функцій додавання,
віднімання, множення та ділення.

1.  Написати функцію create_calculator, яка приймає оператор (наприклад, '+', '-', '*', '/')
    та повертає функцію для виконання обчислень.
2.  Використати цю функцію, щоб створити калькулятор для кількох операцій, і протестувати його.
"""


# ---- Define calculator function creator ----
def create_calculator(operator):
    """
    Return a function to perform arithmetic operations based on the specified operator.

    This function generates and returns an arithmetic function according to the
    operator provided. The supported operations are addition, subtraction,
    multiplication, and division.

    :param operator: Arithmetic operator ("+", "-", "*", "/") to define the function type.
    :type operator: str
    :return: Function that performs the specified arithmetic operation.
    :rtype: function
    """

    def adding(a, b):
        """
        Add two numbers.

        :param a: First number.
        :type a: int or float
        :param b: Second number.
        :type b: int or float
        :return: Sum of a and b.
        :rtype: int or float
        """
        return a + b

    def subtracting(a, b):
        """
        Subtract the second number from the first.

        :param a: First number.
        :type a: int or float
        :param b: Second number.
        :type b: int or float
        :return: Difference of a and b.
        :rtype: int or float
        """
        return a - b

    def multiplying(a, b):
        """
        Multiply two numbers.

        :param a: First number.
        :type a: int or float
        :param b: Second number.
        :type b: int or float
        :return: Product of a and b.
        :rtype: int or float
        """
        return a * b

    def dividing(a, b):
        """
        Divide the first number by the second, handling division by zero.

        :param a: Dividend.
        :type a: int or float
        :param b: Divisor.
        :type b: int or float
        :return: Quotient of a and b, or a message if b is zero.
        :rtype: int, float, or str
        """
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


# ---- Example calculations with predefined operators ----
action = "+"
addition = create_calculator(action)
print(addition(5, 3))
print(addition(10, 5))

action = "-"
subtraction = create_calculator(action)
print(subtraction(5, 3))
print(subtraction(10, 5))

action = "*"
multiplication = create_calculator(action)
print(multiplication(5, 3))
print(multiplication(10, 5))

action = "/"
division = create_calculator(action)
print(division(5, 3))
print(division(10, 0))

# ---- Interactive calculation with user input ----
action = input("Enter operator manually: ")
calculate = create_calculator(action)
x = int(input("Enter first value: "))
y = int(input("Enter second value: "))
print(f"Result: {calculate(x, y)}")
