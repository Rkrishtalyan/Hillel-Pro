def create_calculator(operator):
    def adding(a, b):
        return a + b

    def subtracting(a, b):
        return a - b

    def multiplying(a, b):
        return a * b

    def dividing(a, b):
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
    else:
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
