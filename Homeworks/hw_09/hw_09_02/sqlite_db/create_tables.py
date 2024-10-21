"""
Module for creating tables in the SQLite database.

This module establishes a connection to the SQLite database `school.db` and
creates the `Students`, `Courses`, and `Enrollments` tables if they do not
already exist. It handles potential SQLite errors during the process.

Requires:
    - sqlite3

Functions:
    - create_tables: Creates the required tables for students, courses, and enrollments.
"""

# ---- Imports ----

import sqlite3


# ---- Function Definitions ----

def create_tables():
    """
    Create the 'Students', 'Courses', and 'Enrollments' tables in the 'school.db' SQLite database.

    This function connects to the SQLite database, checks if the tables
    'Students', 'Courses', and 'Enrollments' already exist, and creates
    them if they don't. It ensures that 'student_id' and 'course_id' are
    foreign keys in the 'Enrollments' table, linking it to 'Students' and
    'Courses'.

    :raises sqlite3.Error: If an error occurs during table creation.
    """
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Courses (
                course_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Enrollments (
                enrollment_id INTEGER PRIMARY KEY,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                FOREIGN KEY(student_id) REFERENCES Students(student_id),
                FOREIGN KEY(course_id) REFERENCES Courses(course_id)
            );
        ''')

        conn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while creating tables:", error)
    finally:
        if conn:
            conn.close()
