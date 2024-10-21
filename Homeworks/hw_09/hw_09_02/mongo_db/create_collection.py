"""
Module for creating MongoDB collections.

This module provides functionality for creating a MongoDB connection
and handling potential errors during the process. The connection is
established using the `pymongo` package.

Requires:
    - pymongo.MongoClient
    - pymongo.errors

Functions:
    - create_collections: Connect to a MongoDB instance and select the 'school' database.
"""

# ---- Imports ----

from pymongo import MongoClient, errors


# ---- Function Definitions ----

def create_collections():
    """
    Create a MongoDB connection and select the 'school' database.

    This function attempts to connect to a MongoDB instance running on
    localhost and selects the 'school' database. If there is any error
    during the connection process, it catches a PyMongoError and prints
    the error message.

    :raises pymongo.errors.PyMongoError: If an error occurs while
    connecting to MongoDB.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['school']
        client.close()
    except errors.PyMongoError as e:
        print("Error while connecting to MongoDB:", e)
