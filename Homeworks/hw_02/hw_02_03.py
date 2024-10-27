"""
Завдання 3: Магазин замовлень з акційними знижками.

Написати програму, яка імітує систему замовлення з акціями, де знижки зберігаються
у глобальній області, а нарахування знижки відбувається локально для кожного клієнта.

1.  Створити глобальну змінну discount = 0.1 (10% знижка).
2.  Створити функцію create_order, яка приймає ціну товару як аргумент і всередині:

    - обчислює кінцеву ціну з урахуванням знижки, що визначена глобальною.
    - створює вкладену функцію apply_additional_discount, яка додає додаткову знижку
      (наприклад, для VIP-клієнтів) і змінює фінальну ціну.

3.  Використати ключове слово nonlocal, щоб функція могла змінювати кінцеву ціну у
    вкладеній області видимості.
4.  Після застосування всіх знижок вивести фінальну ціну.
"""

# ---- Set global discount ----
discount = 0.1


# ---- Define order creation function with discount calculations ----
def create_order(sell_price):
    """
    Calculate the net price after applying global and additional VIP discounts.

    This function calculates the net price by first applying a global discount.
    Then, it applies an additional VIP discount within a nested function, either
    cumulatively or by cascading, based on the active code block.

    :param sell_price: Original selling price before any discounts.
    :type sell_price: float
    :return: Final net price after all discounts.
    :rtype: float
    """
    net_price = sell_price - (sell_price * discount)

    def apply_additional_discount():
        """
        Apply a VIP discount to the current net price.

        This function adjusts `net_price` by applying an additional VIP discount. It
        demonstrates two ways of applying the discount: either adding directly to
        the initial discounted price or applying it in a cascading fashion.

        :return: Adjusted net price after VIP discount.
        :rtype: float
        """
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


# ---- Execute order creation with example price ----
create_order(1000)
