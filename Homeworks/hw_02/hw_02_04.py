"""
Завдання 4: Таймер для тренування.

Розробити програму, яка симулює таймер для тренувань із вбудованою функцією,
що дозволяє змінювати час тренування на кожному кроці.

1.  Створити глобальну змінну default_time = 60, яка задає стандартний час
    на кожне тренування (у хвилинах).

2.  Створити функцію training_session, яка:

    - приймає кількість раундів тренування.
    - використовує змінну time_per_round, що відповідає за час на раунд,
      і локально змінює її для кожного тренування.
    - в середині функції створити вкладену функцію adjust_time,
      яка дозволяє налаштовувати час для кожного окремого раунду
      (через неявне використання nonlocal).

3.	Програма повинна виводити тривалість кожного раунду тренування.
"""

# ---- Set default training time ----
default_time = 60


# ---- Define training session function with time adjustment ----
def training_session(rounds):
    """
    Simulate a training session with adjustable round times.

    Each round starts with a default time unless adjusted by the nested function
    `adjust_time`, which decreases the time per round by a set amount and marks
    that the default time is no longer in use.

    :param rounds: Number of training rounds.
    :type rounds: int
    """
    time_per_round = default_time
    is_default_time = True  # Вирішив відтворити приклад використання повністю

    def adjust_time():
        """
        Adjust the time per round by reducing it and marking it as modified.

        This function changes the value of `time_per_round` by decreasing it
        by a fixed amount and updates the `is_default_time` flag to indicate
        that the default time is no longer being used.

        :return: Adjusted time per round.
        :rtype: int
        """
        nonlocal time_per_round
        nonlocal is_default_time
        time_per_round -= 5
        is_default_time = False
        return time_per_round

    for each_round in range(1, rounds + 1):
        if is_default_time:
            print(f'Раунд {each_round}: {time_per_round} хвилин')
        else:
            print(f'Раунд {each_round}: {time_per_round} хвилин (після коригування часу)')
        adjust_time()


# ---- Execute training session with example rounds ----
training_session(3)
