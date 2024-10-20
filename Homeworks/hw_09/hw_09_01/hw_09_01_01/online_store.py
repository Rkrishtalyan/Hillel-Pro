"""
Main execution module for managing products and orders in an online store database.

This script connects to a MongoDB database and performs a series of CRUD operations
and data aggregation tasks for an online store. It includes functionality to:

-   Initialize the database connection and collections.
-   Create new products and orders.
-   Retrieve and print recent orders from the last 30 days.
-   Update product quantities based on a specified order.
-   Delete products with quantities less than or equal to zero.
-   Calculate total products sold within a specified date range.
-   Calculate the total amount spent by specific customers.

Dependencies:

-   pymongo: For MongoDB operations and database connection.
-   datetime: For handling date and time calculations.
-   funcs: A module containing functions for CRUD operations and data aggregation.

Ensure that the MongoDB server is running before executing this script.
"""

from datetime import datetime, timedelta
from pymongo import MongoClient
from funcs import *

# ---- Initialize Database and Client Connection ----
initialize_database()

client = MongoClient("mongodb://localhost:27017/")
db = client["online_store"]
products = db["products"]
orders = db["orders"]

# ---- Create Products and Orders ----

# Additional products
laptop_2 = {
    "name": "Dell XPS 13",
    "price": 85000,
    "category": "laptop",
    "qty_on_hand": 8
}
smartwatch_1 = {
    "name": "Apple Watch Series 9",
    "price": 16000,
    "category": "wearable",
    "qty_on_hand": 25
}

# Additional orders
order_6 = {
    "order_no": 6,
    "customer": "David Gray",
    "items": [
        {"line": 1, "name": "Dell XPS 13", "order_qty": 1},
        {"line": 2, "name": "Apple Watch Series 9", "order_qty": 2}
    ],
    "total_amount": 117000,
    "order_date": datetime.now() - timedelta(days=45)
}

order_7 = {
    "order_no": 7,
    "customer": "Alice Johnson",
    "items": [
        {"line": 1, "name": "iPhone 15 Pro", "order_qty": 1}
    ],
    "total_amount": 49000,
    "order_date": datetime.now() - timedelta(days=20)
}

# ---- CRUD operations ----

# Create products
create_product(products, laptop_2)
create_product(products, smartwatch_1)

# Create orders
create_order(orders, order_6)
create_order(orders, order_7)

# ---- Read Recent Orders (Last 30 Days) ----
read_recent_orders(orders, days=30)

# ---- Update Product Quantities Based on Order ----
update_product_quantity(products, order_7)

# ---- Delete Products Unavailable for Sale (qty_on_hand <= 0) ----
delete_unavailable_products(products)

# ---- Data Aggregation ----

# ---- Total products sold in the last 30 days ----
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()
total_products_sold(orders, start_date, end_date)

# ---- Total amount spent by customer 'John Smith' ----
total_amount_spent_by_customer(orders, 'John Smith')

# ---- Total amount spent by customer 'Alice Johnson' ----
total_amount_spent_by_customer(orders, 'Alice Johnson')

# ---- Close Database Connection ----
client.close()
