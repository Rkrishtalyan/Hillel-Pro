"""Альтернативне рішення"""


# ---- Define product creation function with price update capability ----
def create_product(name):
    """
    Create a product with the specified name, including functionality to set
    the price, quantity, and update the price later.

    :param name: Name of the product.
    :type name: str
    :return: Tuple containing functions to set price and update price.
    :rtype: tuple of functions
    """
    item = {}

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
            Set the quantity of the product and return the product details.

            :param qty: Quantity of the product.
            :type qty: int
            :return: Dictionary containing the product's name, price, and quantity.
            :rtype: dict
            """
            nonlocal item
            item = {
                "name": name,
                "price": sell_price,
                "quantity": qty
            }
            return item

        return set_quantity

    def update_price(new_price):
        """
        Update the price of the product and print the updated price.

        :param new_price: New price to set for the product.
        :type new_price: float or int
        """
        nonlocal item
        item["price"] = new_price
        print(f'\nЦіна товару "{item["name"]}" оновлена до {item["price"]} грн.')

    return set_price, update_price


# ---- Example usage of product creation and price update ----
smartphone_create, smartphone_price_update = create_product("iPhone 15 Pro")
smartphone = smartphone_create(53000)(20)
print(smartphone)

smartphone_price_update(49000)
print(smartphone)
