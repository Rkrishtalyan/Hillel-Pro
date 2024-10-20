"""
Session Tracker Script.

This script demonstrates session creation, retrieval, updating, and deletion
using Redis as the session store. It interacts with the Redis database to
track user session activity, refresh session TTL, and handle session expiration.

Functions used:
- init_database: Initializes the Redis database with sample sessions.
- create_session: Creates or updates a user session.
- get_session: Retrieves session details.
- update_session: Updates session details without changing the session token.
- delete_session: Deletes a session.

Execution Flow:
1. Initialize the database.
2. Create, update, and retrieve sessions for demonstration.
3. Show TTL (time-to-live) for the sessions.
4. Simulate session expiration through sleep.
"""

# ---- Import necessary libraries and functions ----
import time
import redis
from funcs import *

# ---- Initialize the Redis database with sample sessions ----
print("---- Database init started... ----")
wipe_database()
init_database()
print("---- Database init completed. ----")

# ---- Set up Redis client connection ----
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# ---- Demonstration: Create a session for user1 with an updated token ----
print("\n---- Create a session for user1 with an updated token: ----")
create_session('user1', 'updated_token_user1')

session_data = get_session('user1')
if session_data:
    print("\nSession data for user1 after login with new token:")
    for key, value in session_data.items():
        print(f"{key}: {value}")
    ttl = redis_client.ttl('session:user1')
    print(f"TTL for user1's session: {ttl} seconds")

# ---- Simulate user activity after a short delay, then update the session ----
print("\n---- Simulate session update after some time: ----")
time.sleep(2)
update_session('user1')

session_data = get_session('user1')
if session_data:
    print("\nSession data for user1 after activity without token change:")
    for key, value in session_data.items():
        print(f"{key}: {value}")
    ttl = redis_client.ttl('session:user1')
    print(f"TTL for user1's session after activity: {ttl} seconds")

# ---- Delete the session for user1 ----
print("\n---- Delete the session for user1: ----")
delete_session('user1')

session_data = get_session('user1')

# ---- Demonstration: Create a session for user6 with a short TTL ----
print("\n---- Test session expiration for user6: ----")
create_session('user6', 'token6', ttl=5)

session_data = get_session('user6')
if session_data:
    print(f"Session data for user6 after creation:")
    for key, value in session_data.items():
        print(f"{key}: {value}")
    ttl = redis_client.ttl('session:user6')
    print(f"TTL for user6's session: {ttl} seconds")

print("\nWaiting for session to expire...")
time.sleep(6)

session_data = get_session('user6')
if session_data is None:
    print("Session for user6 has expired due to inactivity.")
else:
    print("Session for user6 is still active.")
