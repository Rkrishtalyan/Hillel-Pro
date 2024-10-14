"""
Database initialization module for a movie database.

This module provides a function to initialize an SQLite database using an SQL script
and creates a custom function for generating UUIDs within SQL queries.

Requires:
    sqlite3: A built-in Python module for working with SQLite databases.
    .utils: A custom utility module containing the create_uuid function.

Functions:
    init_database: Initialize the SQLite database and create a custom UUID function.
"""

from .utils import create_uuid
import sqlite3


# ---- Initialize database and set up UUID function ----
def init_database():
    """
    Initialize the SQLite database using a SQL script file.
    Creates a function for generating UUIDs within SQL queries.

    :raises sqlite3.Error: If any error occurs during database interaction.
    """
    try:
        sqlite_connection = sqlite3.connect('movie_database.db')
        cursor = sqlite_connection.cursor()

        with open("movie_database_init.sql", 'r', encoding='utf-8') as script_file:
            init_script = script_file.read()

        sqlite_connection.create_function("uuid", 0, create_uuid)
        cursor.executescript(init_script)

        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error working with SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()
