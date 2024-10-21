"""
CRUD operations for event logs stored in a Cassandra database.

This module provides functions for creating, reading, updating, and deleting event records
from the 'event_logs' table within the 'event_logs' keyspace.
These functions allow you to log events, retrieve events of a specific type, update event metadata,
and delete old events.

Dependencies:
- Cassandra Cluster from `cassandra.cluster`
- UUID generation from `uuid`
- Date and time utilities from `datetime`

Functions:
- `create_event`: Inserts a new event into the database.
- `read_events`: Fetches events based on event type and a specified time range.
- `update_event_metadata`: Updates the metadata for an existing event.
- `delete_old_events`: Deletes events older than a specified number of days.
"""

from datetime import datetime, timedelta
import uuid
from cassandra.cluster import Cluster


def create_event(event_type, user_id, metadata):
    """
    Insert a new event into the event_logs table.

    :param event_type: The type of event (e.g., 'login', 'purchase').
    :type event_type: str
    :param user_id: The UUID of the user who generated the event.
    :type user_id: uuid.UUID
    :param metadata: Additional information about the event.
    :type metadata: str
    :return: The event_id of the newly created event.
    :rtype: uuid.UUID
    :raises Exception: If an error occurs during the event creation process.
    """
    try:
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect('event_logs')

        event_id = uuid.uuid4()
        timestamp = datetime.utcnow()

        session.execute("""
            INSERT INTO event_logs (event_type, timestamp, event_id, user_id, metadata)
            VALUES (%s, %s, %s, %s, %s)
        """, (event_type, timestamp, event_id, user_id, metadata))

        print(f"Event {event_id} created successfully.")
        return event_id

    except Exception as e:
        print("Error creating event:", e)

    finally:
        session.shutdown()
        cluster.shutdown()


def read_events(event_type, date_range_hours=24):
    """
    Retrieve events based on event type and time range.

    This function fetches events of a particular type from the last N hours,
    where N is specified by `date_range_hours`.

    :param event_type: The type of event to filter (e.g., 'login', 'purchase').
    :type event_type: str
    :param date_range_hours: The number of hours to look back for events. Defaults to 24 hours.
    :type date_range_hours: int
    :return: A list of events retrieved from the database.
    :rtype: list
    :raises Exception: If an error occurs while reading events from the database.
    """
    try:
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect('event_logs')

        since_time = datetime.utcnow() - timedelta(hours=date_range_hours)

        rows = session.execute("""
            SELECT event_id, event_type, timestamp, user_id, metadata
            FROM event_logs
            WHERE event_type = %s AND timestamp >= %s
        """, (event_type, since_time))

        events = list(rows)
        print(
            f"Retrieved {len(events)} events of type '{event_type}' from the last {date_range_hours} hours.")
        return events

    except Exception as e:
        print("Error reading events:", e)

    finally:
        session.shutdown()
        cluster.shutdown()


def update_event_metadata(event_id, new_metadata):
    """
    Update the metadata of an existing event.

    This function updates the metadata of an event identified by the event_id.

    :param event_id: The UUID of the event.
    :type event_id: uuid.UUID
    :param new_metadata: The new metadata to replace the existing one.
    :type new_metadata: str
    :raises Exception: If an error occurs while updating the event metadata.
    """
    try:
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect('event_logs')

        # Query to get event_type and timestamp using event_id and return None for proper handling
        row = session.execute("""
            SELECT event_type, timestamp FROM event_logs WHERE event_id = %s
        """, (event_id,)).one()

        if not row:
            print(f"Event {event_id} not found.")
            return

        event_type = row.event_type
        timestamp = row.timestamp

        session.execute("""
            UPDATE event_logs
            SET metadata = %s
            WHERE event_type = %s AND timestamp = %s AND event_id = %s
        """, (new_metadata, event_type, timestamp, event_id))

        print(f"Event {event_id} metadata updated successfully.")

    except Exception as e:
        print("Error updating event metadata:", e)

    finally:
        session.shutdown()
        cluster.shutdown()


def delete_old_events(days=7):
    """
    Delete events older than a specified number of days.

    This function removes all events that are older than the number of days
    specified in the `days` parameter.

    :param days: The number of days before which events will be deleted. Defaults to 7 days.
    :type days: int
    :raises Exception: If an error occurs while deleting old events.
    """
    try:
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect('event_logs')

        cutoff_time = datetime.utcnow() - timedelta(days=days)

        # Get all distinct event_types
        event_type_rows = session.execute("SELECT DISTINCT event_type FROM event_logs")
        event_types = [row.event_type for row in event_type_rows]

        for event_type in event_types:
            session.execute("""
                DELETE FROM event_logs WHERE event_type = %s AND timestamp <= %s
            """, (event_type, cutoff_time))

        print(f"Deleted events older than {days} days.")

    except Exception as e:
        print("Error deleting old events:", e)

    finally:
        session.shutdown()
        cluster.shutdown()
