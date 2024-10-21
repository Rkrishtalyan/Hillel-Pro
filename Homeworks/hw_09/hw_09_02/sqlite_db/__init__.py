"""
Package initializer for the sqlite_db package.

This module imports and exposes the key functions from the
create_tables and sqlite_crud_funcs modules, making it easy to access
the core functionality of the package.

Functions imported from create_tables:
    - create_tables: Creates the necessary tables in the SQLite database.

Functions imported from sqlite_crud_funcs:
    - create_student: Insert a new student record.
    - read_student: Fetch a student record by ID.
    - update_student: Update an existing student record.
    - delete_student: Delete a student record by ID.
    - create_course: Insert a new course record.
    - read_course: Fetch a course record by ID.
    - update_course: Update an existing course record.
    - delete_course: Delete a course record by ID.
    - enroll_student: Insert a new enrollment record.
    - read_enrollment: Fetch an enrollment record by ID.
    - delete_enrollment: Delete an enrollment record by ID.
"""

# ---- Imports ----

from .create_tables import create_tables
from .sqlite_crud_funcs import (
    create_student,
    read_student,
    update_student,
    delete_student,
    create_course,
    read_course,
    update_course,
    delete_course,
    enroll_student,
    read_enrollment,
    delete_enrollment
)
