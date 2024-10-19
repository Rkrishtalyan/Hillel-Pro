"""
Package initializer for managing products and orders in an online store database.

This module imports and exposes key functions from the `database_init` and `crud_funcs` modules,
making them available when the package is imported. The following functionalities are provided:

-   Initialize the database connection and collections.
-   Create new products and orders.
-   Retrieve recent orders placed within a specified number of days.
-   Update product quantities based on orders.
-   Delete products that are no longer available (qty_on_hand <= 0).
-   Calculate the total products sold within a given date range.
-   Calculate the total amount spent by a specific customer.

Modules imported:

-   database_init: Contains functionality to initialize the MongoDB database.
-   crud_funcs: Provides CRUD operations and data aggregation functions
    for managing products and orders in the store.
"""


from .database_init import initialize_database
from .crud_funcs import (
    create_product,
    create_order,
    read_recent_orders,
    update_product_quantity,
    delete_unavailable_products,
    total_products_sold,
    total_amount_spent_by_customer
)

__all__ = [
    'initialize_database',
    'create_product',
    'create_order',
    'read_recent_orders',
    'update_product_quantity',
    'delete_unavailable_products',
    'total_products_sold',
    'total_amount_spent_by_customer'
]
