"""
Завдання 3: Магазин замовлень з акційними знижками.

Написати програму, яка імітує систему замовлення з акціями, де знижки зберігаються у глобальній області,
а нарахування знижки відбувається локально для кожного клієнта.

1.	Створити глобальну змінну discount = 0.1 (10% знижка).
2.	Створити функцію create_order, яка приймає ціну товару як аргумент і всередині:
    - обчислює кінцеву ціну з урахуванням знижки, що визначена глобальною.
    - створює вкладену функцію apply_additional_discount, яка додає додаткову знижку (наприклад, для VIP-клієнтів)
      і змінює фінальну ціну.
3.	Використати ключове слово nonlocal, щоб функція могла змінювати кінцеву ціну у вкладеній області видимості.
4.	Після застосування всіх знижок вивести фінальну ціну.
"""

discount = 0.1


def create_order(sell_price):
    """Calculate and return net_price with global discount applied."""
    net_price = sell_price - (sell_price * discount)

    def apply_additional_discount():
        """Apply additional discount to the net_price."""
        vip_discount = 0.15
        nonlocal net_price
        # якщо сумарная знижка
        net_price = net_price - (sell_price * vip_discount)
        # якщо каскадування знижок
        # net_price = net_price - (net_price * vip_discount)
        return net_price

    apply_additional_discount()
    print(f'Початкова ціна: {sell_price}, кінцева ціна з усіма знижками: {net_price}')
    return net_price


create_order(1000)
