"""
Package initializer for the mongo_db package.

This module imports and exposes the key functions from the
create_collection and mongo_crud_funcs modules, allowing for easier access
to the core functionality of the package.

Functions imported from create_collection:
    - create_collections: Initialize MongoDB collections.

Functions imported from mongo_crud_funcs:
    - create_student: Insert a new student document.
    - read_student: Fetch a student document by ID.
    - update_student: Update an existing student document.
    - delete_student: Delete a student document by ID.
    - create_course: Insert a new course document.
    - read_course: Fetch a course document by ID.
    - update_course: Update an existing course document.
    - delete_course: Delete a course document by ID.
    - enroll_student: Insert a new enrollment document.
    - read_enrollment: Fetch an enrollment document by ID.
    - delete_enrollment: Delete an enrollment document by ID.
"""

# ---- Imports ----

from .create_collection import create_collections
from .mongo_crud_funcs import (
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
