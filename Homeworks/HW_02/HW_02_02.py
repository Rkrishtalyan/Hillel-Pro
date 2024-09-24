"""
Завдання 2: Менеджер підписки на розсилку.

Створити програму, яка імітує менеджер підписки на розсилку, демонструючи роботу з локальними, глобальними
та вкладеними областями видимості.
1.	На глобальному рівні створити змінну subscribers = [] — це список для збереження імен підписників.
2.	Створити функцію subscribe, яка приймає ім'я підписника як аргумент і додає його до списку підписників.
3.	В середині функції subscribe створити вкладену функцію confirm_subscription, яка повертає повідомлення:
    "Підписка підтверджена для <ім'я>".
4.	Створити функцію unsubscribe, яка приймає ім'я та видаляє його зі списку підписників.
    Якщо таке ім'я не знайдено, повертає відповідне повідомлення.
5.	Використати програму для додавання кількох підписників, підтвердження підписки та відписки.
"""


def subscribe(name: str):
    """Add name to subscribers list. Return confirmation message."""
    subscribers.append(name)

    def confirm_subscription(subscriber_name):
        """Print confirmation message."""
        print(f'Підписка підтверджена для {subscriber_name}')

    return confirm_subscription(name)


def unsubscribe(name: str):
    """Attempt to remove name from subscribers list. Print corresponding message."""
    result = ''
    if subscribers.count(name):
        subscribers.remove(name)
        print(f'{name} успішно відписаний')
    else:
        print('Таке імʼя не знайдено')


subscribers = []

subscribe("Олена")
subscribe("Ігор")
print(subscribers)  # ['Олена', 'Ігор']

unsubscribe("Ігор")  # 'Ігор успішно відписаний'
print(subscribers)  # ['Олена']
