"""
Завдання 4: Таймер для тренування.

Розробити програму, яка симулює таймер для тренувань із вбудованою функцією, що дозволяє змінювати час тренування
на кожному кроці.

1.	Створити глобальну змінну default_time = 60, яка задає стандартний час на кожне тренування (у хвилинах).
2.	Створити функцію training_session, яка:
    - приймає кількість раундів тренування.
    - використовує змінну time_per_round, що відповідає за час на раунд, і локально змінює її для кожного тренування.
    - в середині функції створити вкладену функцію adjust_time, яка дозволяє налаштовувати час для кожного
      окремого раунду (через неявне використання nonlocal).
3.	Програма повинна виводити тривалість кожного раунду тренування.
"""

default_time = 60


def training_session(rounds):
    """Set the training duration for each round."""
    time_per_round = default_time
    is_default_time = True  # Вирішив відтворити приклад використання повністю

    def adjust_time():
        """Adjust the duration of each round."""
        nonlocal time_per_round
        nonlocal is_default_time
        time_per_round = time_per_round - 5
        is_default_time = False
        return time_per_round

    for each_round in range(1, rounds + 1):
        if is_default_time:
            print(f'Раунд {each_round}: {time_per_round} хвилин')
        else:
            print(f'Раунд {each_round}: {time_per_round} хвилин (після коригування часу)')
        adjust_time()


training_session(3)
