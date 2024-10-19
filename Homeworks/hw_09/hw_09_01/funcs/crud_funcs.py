"""
Provide CRUD operations and analytics for managing products and orders in a MongoDB database.

This module includes functions to:
- Create products and orders
- Read recent orders
- Update product quantities based on orders
- Delete unavailable products
- Calculate total products sold in a given period
- Calculate total amount spent by a specific customer

Dependencies:

-   datetime: Used for calculating date ranges for recent orders and handling time periods.
-   pymongo.errors: Handles specific exceptions related to MongoDB operations.

Functions:

-   create_product(products_collection, product):
    Inserts a product into the products collection.
-   create_order(orders_collection, order):
    Inserts an order into the orders collection.
-   read_recent_orders(orders_collection, days=30):
    Retrieves and prints orders placed within the last 'days' days.
-   update_product_quantity(products_collection, order):
    Updates the quantities of products based on an order.
-   delete_unavailable_products(products_collection):
    Deletes products no longer available (qty_on_hand <= 0).
-   total_products_sold(orders_collection, start_date, end_date):
    Counts the total number of products sold within a date range.
-   total_amount_spent_by_customer(orders_collection, customer_name):
    Calculates the total sum of all orders for a specific customer.
"""

from datetime import datetime, timedelta
from pymongo import errors


# ---- CRUD Operations ----

# ---- Create Product Function ----
def create_product(products_collection, product):
    """
    Insert a product into the products collection.

    :param products_collection: The MongoDB collection for products.
    :type products_collection: pymongo.collection.Collection
    :param product: A dictionary representing the product to be inserted.
    :type product: dict
    """
    try:
        products_collection.insert_one(product)
        print(f"Inserted product: {product['name']}")
    except errors.DuplicateKeyError:
        print(f"Product already exists: {product['name']}")
    except errors.PyMongoError as e:
        print(f"An error occurred while inserting product '{product['name']}': {e}")


# ---- Create Order Function ----
def create_order(orders_collection, order):
    """
    Insert an order into the orders collection.

    :param orders_collection: The MongoDB collection for orders.
    :type orders_collection: pymongo.collection.Collection
    :param order: A dictionary representing the order to be inserted.
    :type order: dict
    """
    try:
        orders_collection.insert_one(order)
        print(f"Inserted order no: {order['order_no']}")
    except errors.DuplicateKeyError:
        print(f"Order already exists: {order['order_no']}")
    except errors.PyMongoError as e:
        print(f"An error occurred while inserting order no '{order['order_no']}': {e}")


# ---- Read Recent Orders Function ----
def read_recent_orders(orders_collection, days=30):
    """
    Retrieve and print orders placed within the last 'days' days.

    The `order_date` field in each order must be a datetime object for accurate filtering.

    :param orders_collection: The MongoDB collection for orders.
    :type orders_collection: pymongo.collection.Collection
    :param days: The number of days to look back for recent orders. Default is 30 days.
    :type days: int
    """
    print(f"\nOrders from the last {days} days:")
    try:
        date_range = datetime.now() - timedelta(days=days)
        recent_orders = orders_collection.find({"order_date": {"$gte": date_range}})
        for order in recent_orders:
            print(f"Order No: {order['order_no']}, Customer: {order['customer']}, Date: {order['order_date']}")
    except errors.PyMongoError as e:
        print(f"An error occurred while retrieving recent orders: {e}")


# ---- Update Product Quantity Function ----
def update_product_quantity(products_collection, order):
    """
    Update the quantities of products based on the given order.

    Each item in the order should have 'name' (the product name) and 'order_qty' (quantity ordered) keys.

    :param products_collection: The MongoDB collection for products.
    :type products_collection: pymongo.collection.Collection
    :param order: A dictionary representing the order with items to update. Items should include 'name' and 'order_qty'.
    :type order: dict
    """
    print("\nUpdating product quantities based on the order...")
    try:
        for item in order["items"]:
            product_name = item["name"]
            order_qty = item["order_qty"]
            result = products_collection.update_one(
                {"name": product_name},
                {"$inc": {"qty_on_hand": -order_qty}}
            )
            if result.modified_count > 0:
                print(f"Updated '{product_name}' qty_on_hand by -{order_qty}")
            else:
                print(f"No update made for '{product_name}' (product may not exist)")
    except errors.PyMongoError as e:
        print(f"An error occurred while updating product quantities: {e}")


# ---- Delete Unavailable Products Function ----
def delete_unavailable_products(products_collection):
    """
    Delete products from the database that are no longer available (qty_on_hand <= 0).

    :param products_collection: The MongoDB collection for products.
    :type products_collection: pymongo.collection.Collection
    """
    print("\nDeleting products no longer available for sale...")
    try:
        count = products_collection.count_documents({"qty_on_hand": {"$lte": 0}})
        if count == 0:
            print("No products to delete.")
        else:
            unavailable_products = products_collection.find({"qty_on_hand": {"$lte": 0}})
            for product in unavailable_products:
                products_collection.delete_one({"name": product["name"]})
                print(f"Deleted product: {product['name']}")
    except errors.PyMongoError as e:
        print(f"An error occurred while deleting unavailable products: {e}")


# ---- Analytics Functions ----

# ---- Total Products Sold Function ----
def total_products_sold(orders_collection, start_date, end_date):
    """
    Count the total number of products sold between start_date and end_date.

    :param orders_collection: The MongoDB collection for orders.
    :type orders_collection: pymongo.collection.Collection
    :param start_date: The start date of the period.
    :type start_date: datetime.datetime
    :param end_date: The end date of the period.
    :type end_date: datetime.datetime
    """
    print(f"\nTotal products sold from {start_date.date()} to {end_date.date()}:")
    try:
        pipeline = [
            {'$match': {'order_date': {'$gte': start_date, '$lte': end_date}}},
            {'$unwind': '$items'},
            {'$group': {'_id': None, 'total_quantity_sold': {'$sum': '$items.order_qty'}}}
        ]
        result = list(orders_collection.aggregate(pipeline))
        if result:
            total_sold = result[0]['total_quantity_sold']
            print(f"Total products sold: {total_sold}")
            return total_sold
        else:
            print("No products sold in the given period.")
            return 0
    except errors.PyMongoError as e:
        print(f"An error occurred while calculating total products sold: {e}")


# ---- Total Amount Spent by Customer Function ----
def total_amount_spent_by_customer(orders_collection, customer_name):
    """
    Calculate the total sum of all orders for a specific customer.

    :param orders_collection: The MongoDB collection for orders.
    :type orders_collection: pymongo.collection.Collection
    :param customer_name: The name of the customer.
    :type customer_name: str
    """
    print(f"\nCalculating total amount spent by {customer_name}:")
    try:
        pipeline = [
            {'$match': {'customer': customer_name}},
            {'$group': {'_id': '$customer', 'total_spent': {'$sum': '$total_amount'}}}
        ]
        result = list(orders_collection.aggregate(pipeline))
        if result:
            total_spent = result[0]['total_spent']
            print(f"Customer: {customer_name}, Total Amount Spent: {total_spent}")
            return total_spent
        else:
            print(f"No orders found for customer: {customer_name}")
            return 0
    except errors.PyMongoError as e:
        print(f"An error occurred while calculating total amount spent by customer: {e}")
