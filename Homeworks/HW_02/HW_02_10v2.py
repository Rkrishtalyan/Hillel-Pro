# Альтернативне рішення


def create_product(name):
    item = {}

    def set_price(sell_price):
        def set_quantity(qty):
            nonlocal item
            item = {
                "name": name,
                "price": sell_price,
                "quantity": qty
            }
            return item
        return set_quantity

    def update_price(new_price):
        nonlocal item
        item["price"] = new_price
        print(f'\nЦіна товару "{item["name"]}" оновлена до {item["price"]} грн.')

    return set_price, update_price


smartphone_create, smartphone_price_update = create_product("iPhone 15 Pro")
smartphone = smartphone_create(53000)(20)
print(smartphone)

smartphone_price_update(49000)
print(smartphone)
