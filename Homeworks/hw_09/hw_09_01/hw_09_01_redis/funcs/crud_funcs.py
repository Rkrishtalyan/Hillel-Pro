"""
CRUD operations for managing user sessions in Redis.

This module provides functions to create, update, retrieve, and delete
user sessions stored in a Redis database. Each session includes a session
token, login time, and last activity time, and can be updated or deleted
as needed.

:raises redis.ConnectionError: If there is an issue connecting to Redis.
:raises Exception: For any other errors encountered during execution.
"""

# ---- Import necessary libraries ----
import time
import redis

# ---- Function to create a new session or update an existing one ----
def create_session(user_id, session_token, ttl=1800):
    """
    Create a new session for the user or update an existing one.

    If a session for the user does not exist, a new session is created with a session token,
    login time, and last activity time. If the session already exists, it is updated by
    refreshing the session token and login time.

    :param user_id: The unique identifier for the user.
    :type user_id: str
    :param session_token: The token for the session.
    :type session_token: str
    :param ttl: Time-to-live for the session in seconds. Defaults to 1800 (30 minutes).
    :type ttl: int
    :raises redis.ConnectionError: If there is an issue connecting to Redis.
    :raises Exception: For any other errors encountered during execution.
    """
    try:
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        session_key = f'session:{user_id}'

        if not redis_client.exists(session_key):
            # Create a new session
            current_time = int(time.time())
            redis_client.hset(session_key, mapping={
                'session_token': session_token,
                'login_time': current_time,
                'last_activity_time': current_time
            })
            redis_client.expire(session_key, ttl)
            print(f"Session for {user_id} has been created with TTL of {ttl} seconds.")
        else:
            # Session exists; update it by calling update_session
            print(f"Session for {user_id} already exists. Updating login_time, session_token, and refreshing session.")
            update_session(user_id, session_token=session_token, update_login_time=True)
    except redis.ConnectionError as error:
        print("Error connecting to Redis:", error)
    except Exception as error:
        print("An error occurred:", error)

# ---- Function to update an existing session ----
def update_session(user_id, session_token=None, update_login_time=False):
    """
    Update the session for a user.

    This function updates the session token, login time (if specified),
    and the last activity time for the session.
    If the session does not exist, no update is made.

    :param user_id: The unique identifier for the user.
    :type user_id: str
    :param session_token: The token to update in the session. Defaults to None.
    :type session_token: str, optional
    :param update_login_time: Flag to update the login time. Defaults to False.
    :type update_login_time: bool, optional
    :raises redis.ConnectionError: If there is an issue connecting to Redis.
    :raises Exception: For any other errors encountered during execution.
    """
    try:
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        session_key = f'session:{user_id}'

        if redis_client.exists(session_key):
            current_time = int(time.time())
            update_fields = {'last_activity_time': current_time}
            if session_token:
                update_fields['session_token'] = session_token
            if update_login_time:
                update_fields['login_time'] = current_time
            redis_client.hset(session_key, mapping=update_fields)
            redis_client.expire(session_key, 1800)
            print(f"Session for {user_id} has been updated and TTL refreshed.")
        else:
            print(f"No active session for {user_id} to update.")
    except redis.ConnectionError as error:
        print("Error connecting to Redis:", error)
    except Exception as error:
        print("An error occurred:", error)

# ---- Function to retrieve session details for a user ----
def get_session(user_id):
    """
    Retrieve the session details for a user.

    This function fetches the session data for the given user if it exists.
    The session data includes session token, login time, and last activity time.

    :param user_id: The unique identifier for the user.
    :type user_id: str
    :return: A dictionary containing session data or None if no session exists.
    :rtype: dict or None
    :raises redis.ConnectionError: If there is an issue connecting to Redis.
    :raises Exception: For any other errors encountered during execution.
    """
    try:
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        session_key = f'session:{user_id}'

        if redis_client.exists(session_key):
            session_data = redis_client.hgetall(session_key)
            session_data = {k.decode('utf-8'): v.decode('utf-8') for k, v in session_data.items()}
            return session_data
        else:
            print(f"No active session for {user_id}.")
            return None
    except redis.ConnectionError as error:
        print("Error connecting to Redis:", error)
        return None
    except Exception as error:
        print("An error occurred:", error)
        return None

# ---- Function to delete a session ----
def delete_session(user_id):
    """
    Delete the session for a user.

    This function removes the session data for the given user if it exists.

    :param user_id: The unique identifier for the user.
    :type user_id: str
    :raises redis.ConnectionError: If there is an issue connecting to Redis.
    :raises Exception: For any other errors encountered during execution.
    """
    try:
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        session_key = f'session:{user_id}'

        if redis_client.exists(session_key):
            redis_client.delete(session_key)
            print(f"Session for {user_id} has been deleted.")
        else:
            print(f"No active session for {user_id} to delete.")
    except redis.ConnectionError as error:
        print("Error connecting to Redis:", error)
    except Exception as error:
        print("An error occurred:", error)
