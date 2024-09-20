def subscribe(name: str):
    subscribers.append(name)

    def confirm_subscription(subscriber_name):
        print(f'Підписка підтверджена для {subscriber_name}')

    return confirm_subscription(name)


def unsubscribe(name: str):
    result = ''
    if subscribers.count(name):
        subscribers.remove(name)
        result = f'{name} успішно відписаний'
    else:
        result = 'Таке імʼя не знайдено'
    return result


subscribers = []

subscribe("Олена")
subscribe("Ігор")
print(subscribers)  # ['Олена', 'Ігор']
print(unsubscribe("Ігор"))  # 'Ігор успішно відписаний'
print(subscribers)  # ['Олена']
