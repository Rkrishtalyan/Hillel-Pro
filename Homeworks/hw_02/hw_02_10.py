"""
Завдання 10: Створення товарів для онлайн-магазину.

Розробити програму для управління товарами в онлайн-магазині, використовучи карирувані функції.

1.  Написати функцію create_product, яка приймає назву, ціну та кількість товару.
2.  Використати замикання для створення функції, яка дозволяє змінювати ціну товару.
"""


# ---- Define product creation function ----
def create_product(name):
    """
    Create a product with the specified name and return a function to set its price.

    :param name: Name of the product.
    :type name: str
    :return: Function to set the product's price.
    :rtype: function
    """
    def set_price(sell_price):
        """
        Set the product's price and return a function to set its quantity.

        :param sell_price: Selling price of the product.
        :type sell_price: float or int
        :return: Function to set the product's quantity.
        :rtype: function
        """
        def set_quantity(qty):
            """
            Set the quantity of the product and return a dictionary with product details.

            :param qty: Quantity of the product.
            :type qty: int
            :return: Dictionary containing the product's name, price, and quantity.
            :rtype: dict
            """
            item = {
                "name": name,
                "price": sell_price,
                "quantity": qty
            }
            return item

        return set_quantity

    return set_price


# ---- Define price management function ----
def price_manager(item):
    """
    Return a function to update the price of a given product item.

    :param item: Dictionary representing the product.
    :type item: dict
    :return: Function to update the product's price.
    :rtype: function
    """
    def update_price(new_price):
        """
        Update the price of the product and print the updated price.

        :param new_price: New price to set for the product.
        :type new_price: float or int
        """
        nonlocal item
        item["price"] = new_price
        print(f'\nЦіна товару "{item["name"]}" оновлена до {item["price"]} грн.')

    return update_price


# ---- Example usage of product creation and price management ----
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
