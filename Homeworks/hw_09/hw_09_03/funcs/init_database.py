"""
Initialize the event_logs keyspace and table for storing event logs.

This module connects to a Cassandra database, creates a keyspace if it doesn't exist,
and sets up a table called 'event_logs' for storing various events.
It also inserts a set of sample data representing user activity events such as
login, logout, purchases, and views.

Dependencies:
- Cassandra Cluster from `cassandra.cluster`
- UUID generation from `uuid`
- Date and time utilities from `datetime`

Usage:
Call `initialize_database()` to create the keyspace and table, and insert sample data.
"""

import uuid
from datetime import datetime, timedelta
from cassandra.cluster import Cluster


def initialize_database():
    """
    Initialize the Cassandra database with a keyspace and event_logs table.

    This function connects to a Cassandra instance, creates the keyspace and table
    if they don't exist, and inserts some predefined sample data representing events.

    :raises Exception: If there's an error during the database setup.
    """
    try:
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect()

        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS event_logs
            WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
        """)
        session.set_keyspace('event_logs')

        # Create the event_logs table with adjusted primary key
        session.execute("""
            CREATE TABLE IF NOT EXISTS event_logs (
                event_type text,
                timestamp timestamp,
                event_id uuid,
                user_id uuid,
                metadata text,
                PRIMARY KEY ((event_type), timestamp, event_id)
            ) WITH CLUSTERING ORDER BY (timestamp DESC);
        """)

        session.execute("""
            CREATE INDEX IF NOT EXISTS ON event_logs (event_id);
        """)

        sample_data = [
            ('login', datetime.utcnow() - timedelta(hours=1), uuid.uuid4(), uuid.uuid4(), 'User logged in'),
            ('logout', datetime.utcnow() - timedelta(hours=2), uuid.uuid4(), uuid.uuid4(), 'User logged out'),
            ('purchase', datetime.utcnow() - timedelta(days=1), uuid.uuid4(), uuid.uuid4(), 'User purchased item'),
            ('login', datetime.utcnow() - timedelta(days=2), uuid.uuid4(), uuid.uuid4(), 'User logged in from mobile'),
            ('view', datetime.utcnow() - timedelta(hours=10), uuid.uuid4(), uuid.uuid4(), 'User viewed page'),
            ('click', datetime.utcnow() - timedelta(hours=3), uuid.uuid4(), uuid.uuid4(), 'User clicked ad'),
            ('purchase', datetime.utcnow() - timedelta(days=5), uuid.uuid4(), uuid.uuid4(), 'User bought subscription'),
            ('login', datetime.utcnow() - timedelta(days=7), uuid.uuid4(), uuid.uuid4(), 'User logged in via API'),
            ('logout', datetime.utcnow() - timedelta(hours=4), uuid.uuid4(), uuid.uuid4(),
             'User logged out from desktop'),
            ('view', datetime.utcnow() - timedelta(hours=12), uuid.uuid4(), uuid.uuid4(), 'User viewed new feature')
        ]

        for event in sample_data:
            event_type, timestamp, event_id, user_id, metadata = event

            session.execute("""
                INSERT INTO event_logs (event_type, timestamp, event_id, user_id, metadata)
                VALUES (%s, %s, %s, %s, %s)
            """, (event_type, timestamp, event_id, user_id, metadata))

        print("Database initialized with sample data.")

    except Exception as e:
        print("Error initializing database:", e)

    finally:
        session.shutdown()
        cluster.shutdown()
