"""
Завдання 2: Менеджер підписки на розсилку.

Створити програму, яка імітує менеджер підписки на розсилку, демонструючи роботу з локальними,
глобальними та вкладеними областями видимості.

1.  На глобальному рівні створити змінну subscribers = [] —
    це список для збереження імен підписників.
2.  Створити функцію subscribe, яка приймає ім'я підписника як аргумент
    і додає його до списку підписників.
3.  В середині функції subscribe створити вкладену функцію confirm_subscription,
    яка повертає повідомлення: "Підписка підтверджена для <ім'я>".
4.  Створити функцію unsubscribe, яка приймає ім'я та видаляє його зі списку підписників.
    Якщо таке ім'я не знайдено, повертає відповідне повідомлення.
5.  Використати програму для додавання кількох підписників, підтвердження підписки та відписки.
"""


# ---- Define subscriber management functions ----
def subscribe(name: str):
    """
    Add a subscriber to the subscribers list and confirm the subscription.

    This function appends a new subscriber's name to the global list 'subscribers'
    and prints a confirmation message.

    :param name: Name of the subscriber to add.
    :type name: str
    """
    subscribers.append(name)

    def confirm_subscription(subscriber_name):
        """
        Print a confirmation message for the given subscriber.

        :param subscriber_name: Name of the subscriber whose subscription is confirmed.
        :type subscriber_name: str
        """
        print(f'Підписка підтверджена для {subscriber_name}')

    return confirm_subscription(name)


def unsubscribe(name: str):
    """
    Remove a subscriber from the subscribers list if present and confirm the unsubscription.

    If the specified name is found in the 'subscribers' list, it is removed, and a confirmation
    message is printed. If the name is not found, an error message is displayed.

    :param name: Name of the subscriber to remove.
    :type name: str
    """
    if subscribers.count(name):
        subscribers.remove(name)
        print(f'{name} успішно відписаний')
    else:
        print('Таке імʼя не знайдено')


# ---- Main code execution ----
subscribers = []

subscribe("Олена")
subscribe("Ігор")
print(subscribers)  # ['Олена', 'Ігор']

unsubscribe("Ігор")  # 'Ігор успішно відписаний'
print(subscribers)  # ['Олена']
