discount = 0.1


def create_order(sell_price):
    net_price = sell_price - (sell_price * discount)

    def apply_additional_discount():
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
