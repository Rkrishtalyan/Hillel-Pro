"""
Module for performing CRUD operations on SQLite database tables.

This module provides functions to create, read, update, and delete
records from the 'Students', 'Courses', and 'Enrollments' tables in
the SQLite database `school.db`. It handles SQLite-related errors
gracefully.

Requires:
    - sqlite3

Functions:
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

import sqlite3


# ---- CRUD Operations for Students ----

def create_student(student_id, name, email):
    """
    Insert a new student into the 'Students' table.

    :param student_id: Unique ID of the student.
    :type student_id: int
    :param name: Name of the student.
    :type name: str
    :param email: Email of the student.
    :type email: str
    :raises sqlite3.IntegrityError: If student ID or email is not unique.
    :raises sqlite3.Error: For other SQLite-related errors.
    """
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Students (student_id, name, email) VALUES (?, ?, ?);
        ''', (student_id, name, email))

        conn.commit()
        cursor.close()

    except sqlite3.IntegrityError:
        print(f"Student with ID {student_id} already exists or email is not unique.")
    except sqlite3.Error as error:
        print("Error while creating student:", error)
    finally:
        if conn:
            conn.close()


def read_student(student_id):
    """
    Fetch a student record by ID from the 'Students' table.

    :param student_id: The ID of the student to fetch.
    :type student_id: int
    :return: The student record as a dictionary or None if not found.
    :rtype: dict or None
    :raises sqlite3.Error: For any SQLite-related errors.
    """
    try:
        conn = sqlite3.connect('school.db')
        conn.row_factory = sqlite3.Row  # Enable accessing columns by name
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM Students WHERE student_id = ?;
        ''', (student_id,))

        row = cursor.fetchone()
        cursor.close()
        if row:
            student = dict(row)
            return student
        else:
            return None

    except sqlite3.Error as error:
        print("Error while reading student:", error)
    finally:
        if conn:
            conn.close()


def update_student(student_id, name, email):
    """
    Update an existing student record in the 'Students' table.

    :param student_id: The ID of the student to update.
    :type student_id: int
    :param name: Updated name of the student.
    :type name: str
    :param email: Updated email of the student.
    :type email: str
    :raises sqlite3.Error: For any SQLite-related errors.
    """
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE Students SET name = ?, email = ? WHERE student_id = ?;
        ''', (name, email, student_id))

        conn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while updating student:", error)
    finally:
        if conn:
            conn.close()


def delete_student(student_id):
    """
    Delete a student record by ID from the 'Students' table.

    :param student_id: The ID of the student to delete.
    :type student_id: int
    :raises sqlite3.Error: For any SQLite-related errors.
    """
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM Students WHERE student_id = ?;
        ''', (student_id,))

        conn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while deleting student:", error)
    finally:
        if conn:
            conn.close()


# ---- CRUD Operations for Courses ----

def create_course(course_id, title, description):
    """
    Insert a new course into the 'Courses' table.

    :param course_id: Unique ID of the course.
    :type course_id: int
    :param title: Title of the course.
    :type title: str
    :param description: Description of the course.
    :type description: str
    :raises sqlite3.IntegrityError: If course ID already exists.
    :raises sqlite3.Error: For other SQLite-related errors.
    """
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Courses (course_id, title, description) VALUES (?, ?, ?);
        ''', (course_id, title, description))

        conn.commit()
        cursor.close()

    except sqlite3.IntegrityError:
        print(f"Course with ID {course_id} already exists.")
    except sqlite3.Error as error:
        print("Error while creating course:", error)
    finally:
        if conn:
            conn.close()


def read_course(course_id):
    """
    Fetch a course record by ID from the 'Courses' table.

    :param course_id: The ID of the course to fetch.
    :type course_id: int
    :return: The course record as a dictionary or None if not found.
    :rtype: dict or None
    :raises sqlite3.Error: For any SQLite-related errors.
    """
    try:
        conn = sqlite3.connect('school.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM Courses WHERE course_id = ?;
        ''', (course_id,))

        row = cursor.fetchone()
        cursor.close()
        if row:
            course = dict(row)
            return course
        else:
            return None

    except sqlite3.Error as error:
        print("Error while reading course:", error)
    finally:
        if conn:
            conn.close()


def update_course(course_id, title, description):
    """
    Update an existing course record in the 'Courses' table.

    :param course_id: The ID of the course to update.
    :type course_id: int
    :param title: Updated title of the course.
    :type title: str
    :param description: Updated description of the course.
    :type description: str
    :raises sqlite3.Error: For any SQLite-related errors.
    """
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE Courses SET title = ?, description = ? WHERE course_id = ?;
        ''', (title, description, course_id))

        conn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while updating course:", error)
    finally:
        if conn:
            conn.close()


def delete_course(course_id):
    """
    Delete a course record by ID from the 'Courses' table.

    :param course_id: The ID of the course to delete.
    :type course_id: int
    :raises sqlite3.Error: For any SQLite-related errors.
    """
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM Courses WHERE course_id = ?;
        ''', (course_id,))

        conn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while deleting course:", error)
    finally:
        if conn:
            conn.close()


# ---- CRUD Operations for Enrollments ----

def enroll_student(enrollment_id, student_id, course_id):
    """
    Insert a new enrollment into the 'Enrollments' table.

    :param enrollment_id: Unique ID of the enrollment.
    :type enrollment_id: int
    :param student_id: The student's ID.
    :type student_id: int
    :param course_id: The course ID.
    :type course_id: int
    :raises sqlite3.IntegrityError: If enrollment ID already exists or foreign key constraint fails.
    :raises sqlite3.Error: For other SQLite-related errors.
    """
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Enrollments (enrollment_id, student_id, course_id) VALUES (?, ?, ?);
        ''', (enrollment_id, student_id, course_id))

        conn.commit()
        cursor.close()

    except sqlite3.IntegrityError:
        print(f"Enrollment with ID {enrollment_id} already exists or foreign key constraint failed.")
    except sqlite3.Error as error:
        print("Error while enrolling student:", error)
    finally:
        if conn:
            conn.close()


def read_enrollment(enrollment_id):
    """
    Fetch an enrollment record by ID from the 'Enrollments' table.

    :param enrollment_id: The ID of the enrollment to fetch.
    :type enrollment_id: int
    :return: The enrollment record as a dictionary or None if not found.
    :rtype: dict or None
    :raises sqlite3.Error: For any SQLite-related errors.
    """
    try:
        conn = sqlite3.connect('school.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM Enrollments WHERE enrollment_id = ?;
        ''', (enrollment_id,))

        row = cursor.fetchone()
        cursor.close()
        if row:
            enrollment = dict(row)
            return enrollment
        else:
            return None

    except sqlite3.Error as error:
        print("Error while reading enrollment:", error)
    finally:
        if conn:
            conn.close()


def delete_enrollment(enrollment_id):
    """
    Delete an enrollment record by ID from the 'Enrollments' table.

    :param enrollment_id: The ID of the enrollment to delete.
    :type enrollment_id: int
    :raises sqlite3.Error: For any SQLite-related errors.
    """
    try:
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM Enrollments WHERE enrollment_id = ?;
        ''', (enrollment_id,))

        conn.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while deleting enrollment:", error)
    finally:
        if conn:
            conn.close()
