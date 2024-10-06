from . import *  # довелося запустити main.py як модуль, а не скрипт, щоб працював відносний імпорт
from . import remove_whitespaces

# math_utils functions
print(factorial(10))
print(gcd(48, 16))

# string_utils functions
print(all_upper("don't yell at me"))
print(remove_whitespaces("      ...please      "))
