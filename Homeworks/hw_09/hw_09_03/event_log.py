# main.py

"""
Main execution script for demonstrating CRUD operations on event logs.

This script demonstrates the following operations:
1. Initializing the Cassandra database.
2. Creating a new event.
3. Reading events.
4. Updating the metadata of an existing event.
5. Deleting old events.

Dependencies:
- `uuid` for generating unique user IDs.
- `crud_funcs` for database and event log operations.
"""

import uuid
from funcs import *

# ---- Initialize the database ----
initialize_database()

# ---- Demonstrate Create operation ----
print("\n---- Create Operation ----")
user_id = uuid.uuid4()
created_event_id = create_event('login', user_id, 'User logged in via mobile')

# ---- Demonstrate Read operation ----
print("\n---- Read Operation ----")
events = read_events('login')
for event in events:
    print(f"Event ID: {event.event_id}, Event Type: {event.event_type}, Timestamp: {event.timestamp}, User ID: {event.user_id}, Metadata: {event.metadata}")

# ---- Demonstrate Update operation ----
print("\n---- Update Operation ----")
update_event_metadata(
    created_event_id,
    'Updated metadata with more details'
)

# ---- Demonstrate Delete operation ----
print("\n---- Delete Operation ----")
delete_old_events(days=7)
