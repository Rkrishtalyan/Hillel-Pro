"""
Initialize the Redis database with sample user sessions.

This module connects to a Redis instance and creates session data for a list
of sample users. If a session already exists for a user, the session creation is skipped.
Each session includes a session token, login time, and last activity time.
The session data expires after 1800 seconds (30 minutes).

:raises redis.ConnectionError: If there is an issue connecting to Redis.
:raises Exception: For any other errors encountered during execution.
"""

# ---- Import necessary libraries ----
import time
import redis

# ---- Initialize the database with sample user sessions ----
def init_database():
    """
    Initialize Redis database with sample user sessions.

    This function attempts to connect to Redis and populate the database with sample user session data.
    It checks whether a session already exists for each user and creates one if necessary.

    :raises redis.ConnectionError: If there is an issue connecting to Redis.
    :raises Exception: For any other errors encountered during execution.
    """
    try:
        redis_client = redis.Redis(host='localhost', port=6379, db=0)

        sample_users = [
            {'user_id': 'user1', 'session_token': 'token1'},
            {'user_id': 'user2', 'session_token': 'token2'},
            {'user_id': 'user3', 'session_token': 'token3'},
            {'user_id': 'user4', 'session_token': 'token4'},
            {'user_id': 'user5', 'session_token': 'token5'},
        ]

        for user in sample_users:
            session_key = f'session:{user["user_id"]}'

            if not redis_client.exists(session_key):
                current_time = int(time.time())
                redis_client.hset(session_key, mapping={
                    'session_token': user['session_token'],
                    'login_time': current_time,
                    'last_activity_time': current_time
                })
                redis_client.expire(session_key, 1800)
                print(f"Session for {user['user_id']} has been created.")
            else:
                print(f"Session for {user['user_id']} already exists. Skipping creation.")

    except redis.ConnectionError as error:
        print("Error connecting to Redis:", error)

    except Exception as error:
        print("An error occurred:", error)
