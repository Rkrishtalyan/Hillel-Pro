"""
Module for initializing and populating an online store database.

This module connects to a MongoDB database, creates necessary collections
and indexes, and populates the database with sample product and order data.
Duplicate entries are ignored during insertion.

Functions:
- initialize_database: Initializes the database, sets up indexes, and populates sample data.

Dependencies:
- pymongo for MongoDB operations
- datetime for date and time manipulation

Ensure that the MongoDB server is running before executing this module.
"""

from datetime import datetime, timedelta
from pymongo import MongoClient, errors

# ---- Initialize and populate the database ----
def initialize_database():
    """
    Initialize the database and populate it with initial product and order data.

    This function connects to a MongoDB database, creates necessary indexes for
    products and orders collections, and inserts sample product and order data.
    Duplicate entries are ignored during insertion.

    :raises errors.PyMongoError: If any error occurs during database operations.
    """
    try:
        client = MongoClient("mongodb://localhost:27017/")

        # ---- Create the database and collections ----
        db = client["online_store"]
        products = db["products"]
        orders = db["orders"]

        # ---- Create indexes for unique fields ----
        products.create_index("name", unique=True)
        products.create_index("category")
        orders.create_index("order_no", unique=True)

        # ---- Define sample product data ----
        phone_1 = {
            "name": "iPhone 15 Pro",
            "price": 49000,
            "category": "phone",
            "qty_on_hand": 10
        }
        phone_2 = {
            "name": "Samsung Galaxy S23",
            "price": 42000,
            "category": "phone",
            "qty_on_hand": 15
        }
        laptop_1 = {
            "name": "MacBook Pro 16",
            "price": 95000,
            "category": "laptop",
            "qty_on_hand": 5
        }
        tablet_1 = {
            "name": "iPad Air",
            "price": 25000,
            "category": "tablet",
            "qty_on_hand": 12
        }
        headphones_1 = {
            "name": "Sony WH-1000XM5",
            "price": 12000,
            "category": "accessory",
            "qty_on_hand": 20
        }

        # ---- Define sample order data ----
        order_1 = {
            "order_no": 1,
            "customer": "John Smith",
            "items": [
                {"line": 1, "name": "iPhone 15 Pro", "order_qty": 1},
                {"line": 2, "name": "MacBook Pro 16", "order_qty": 1}
            ],
            "total_amount": 144000,
            "order_date": datetime.now() - timedelta(days=25)
        }

        order_2 = {
            "order_no": 2,
            "customer": "Jane Doe",
            "items": [
                {"line": 1, "name": "Samsung Galaxy S23", "order_qty": 1},
                {"line": 2, "name": "Sony WH-1000XM5", "order_qty": 2}
            ],
            "total_amount": 66000,
            "order_date": datetime.now() - timedelta(days=40)
        }

        order_3 = {
            "order_no": 3,
            "customer": "Alice Johnson",
            "items": [
                {"line": 1, "name": "iPad Air", "order_qty": 1}
            ],
            "total_amount": 25000,
            "order_date": datetime.now() - timedelta(days=10)
        }

        order_4 = {
            "order_no": 4,
            "customer": "John Smith",
            "items": [
                {"line": 1, "name": "iPhone 15 Pro", "order_qty": 2},
                {"line": 2, "name": "Sony WH-1000XM5", "order_qty": 1}
            ],
            "total_amount": 110000,
            "order_date": datetime.now() - timedelta(days=35)
        }

        order_5 = {
            "order_no": 5,
            "customer": "Charlie Green",
            "items": [
                {"line": 1, "name": "MacBook Pro 16", "order_qty": 1},
                {"line": 2, "name": "iPad Air", "order_qty": 2},
                {"line": 3, "name": "Sony WH-1000XM5", "order_qty": 1}
            ],
            "total_amount": 147000,
            "order_date": datetime.now() - timedelta(days=5)
        }

        # ---- Insert products into the collection ----
        product_list = [phone_1, phone_2, laptop_1, tablet_1, headphones_1]
        for product in product_list:
            try:
                products.insert_one(product)
            except errors.DuplicateKeyError:
                pass  # Ignore duplicate entries

        # ---- Insert orders into the collection ----
        order_list = [order_1, order_2, order_3, order_4, order_5]
        for order in order_list:
            try:
                orders.insert_one(order)
            except errors.DuplicateKeyError:
                pass  # Ignore duplicate entries

    except errors.PyMongoError as e:
        print("An error occurred:", e)

    finally:
        client.close()
