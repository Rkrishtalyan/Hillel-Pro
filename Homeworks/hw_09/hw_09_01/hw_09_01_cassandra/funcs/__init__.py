"""
Initialization module for the event logging package.

This module imports and exposes the key functions for initializing the database
and performing CRUD operations on the event logs. It ensures that only the relevant
functions are made available when the package is imported.

Exposed functions:
- `initialize_database`: Sets up the Cassandra database and event log table.
- `create_event`: Inserts a new event into the event logs.
- `read_events`: Fetches events based on user ID, event type, and time range.
- `update_event_metadata`: Updates the metadata of an existing event.
- `delete_old_events`: Deletes events older than a specified number of days.
"""

from .init_database import initialize_database
from .crud_funcs import create_event, read_events, update_event_metadata, delete_old_events

__all__ = [
    'initialize_database',
    'create_event',
    'read_events',
    'update_event_metadata',
    'delete_old_events'
]
