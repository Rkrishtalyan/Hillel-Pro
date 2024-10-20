"""
Module to wipe the Redis database.

This module provides a function to clear all data in the specified Redis database.
It connects to the Redis instance and performs a flush operation to delete all keys.

:raises redis.ConnectionError: If there is an issue connecting to Redis.
:raises Exception: For any other errors encountered during execution.
"""

# ---- Import necessary library ----
import redis

# ---- Function to wipe the Redis database ----
def wipe_database():
    """
    Wipe the Redis database by flushing all data.

    This function connects to a Redis instance and clears all data by calling
    the `flushdb` command, which removes all keys from the selected Redis database.

    :raises redis.ConnectionError: If there is an issue connecting to Redis.
    :raises Exception: For any other errors encountered during execution.
    """
    try:
        redis_client = redis.Redis(host='localhost', port=6379, db=0)

        redis_client.flushdb()
        print("Database has been wiped clean.")

    except redis.ConnectionError as error:
        print("Error connecting to Redis:", error)
    except Exception as error:
        print("An error occurred:", error)
