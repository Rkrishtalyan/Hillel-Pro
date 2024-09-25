"""
Завдання 10: Створення товарів для онлайн-магазину.

Розробити програму для управління товарами в онлайн-магазині, використовучи карирувані функції.

1.	Написати функцію create_product, яка приймає назву, ціну та кількість товару.
2.	Використати замикання для створення функції, яка дозволяє змінювати ціну товару.
"""


def create_product(name):
    """Populate product details via currying function call. Return dict."""
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
    """Create and return price managing functions."""
    def update_price(new_price):
        """Update product price. Print corresponding message."""
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
