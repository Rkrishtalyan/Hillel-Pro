"""
Завдання 3: Інспекція модулів

Напишіть програму, яка приймає на вхід назву модуля (рядок) та виводить список усіх класів, функцій
та їхніх сигнатур у модулі. Використовуйте модуль inspect.
"""

import inspect
import importlib


def analyze_module(module_name: str):
    """
    Analyze the functions and classes of a given module by its name.

    This function imports the specified module, retrieves its members, and prints
    the list of functions and classes present in the module. If the module cannot
    be imported, it prints an error message.

    :param module_name: The name of the module to be analyzed.
    :type module_name: str
    """
    try:
        module = importlib.import_module(module_name)
    except ImportError:
        print(f"Module {module_name} not found.")
        return

    members = inspect.getmembers(module)

    functions = []
    classes = []

    for name, value in members:
        if name.startswith("__"):
            continue

        if inspect.isfunction(value) or inspect.isbuiltin(value):
            functions.append((name, value))
        elif inspect.isclass(value):
            classes.append((name, value))

    print("\nFunctions:")
    if functions:
        for func_name, func in functions:
            sig = ""
            try:
                sig = inspect.signature(func)
            except ValueError:
                pass
            print(f"- {func_name}{sig}")
    else:
        print("Functions list is empty.")

    print("\nClasses:")
    if classes:
        for cls_name, cls in classes:
            print(f"- {cls_name}")
    else:
        print("Classes list is empty.")


analyze_module("math")
