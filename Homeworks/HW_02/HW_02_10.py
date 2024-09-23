def create_product(name):
    def set_price(sell_price):
        def set_quantity(qty):
            item = {
                "name": name,
                "price": sell_price,
                "quantity": qty
            }
            return item
        return set_quantity
    return set_price


def price_manager(item):
    def update_price(new_price):
        nonlocal item
        item["price"] = new_price
        print(f'\nЦіна товару "{item["name"]}" оновлена до {item["price"]} грн.')

    return update_price


smartphone = create_product("iPhone 15 Pro")(53000)(50)
print(f'\n{smartphone["name"]}, ціна {smartphone["price"]}, кількість {smartphone["quantity"]}')

update_smartphone_price = price_manager(smartphone)
update_smartphone_price(49000)
print(f'\n{smartphone["name"]}, ціна {smartphone["price"]}, кількість {smartphone["quantity"]}')

print()

laptop = create_product("Asus Rog Strix 17")(108000)(10)
print(laptop)

update_laptop_price = price_manager(laptop)
update_laptop_price(115000)
print(laptop)
