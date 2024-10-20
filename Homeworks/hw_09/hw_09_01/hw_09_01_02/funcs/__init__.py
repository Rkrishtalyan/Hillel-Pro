"""
Initialize the package with essential functions.

This `__init__.py` file imports the core functions for initializing the Redis database
and performing CRUD operations on user sessions. The `__all__` variable explicitly defines
the public API of the package.

Available functions:
- init_database
- create_session
- get_session
- update_session
- delete_session
"""

# ---- Import key functions from package modules ----
from .init_database import init_database
from .wipe_database import wipe_database
from .crud_funcs import create_session, get_session, update_session, delete_session

# ---- Define the public API for the package ----
__all__ = [
    'init_database',
    'wipe_database',
    'create_session',
    'update_session',
    'get_session',
    'delete_session'
]
