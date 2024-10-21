"""
Module for performing CRUD operations on MongoDB collections.

This module provides functions to create, read, update, and delete
documents in MongoDB collections, including 'students', 'courses',
and 'enrollments'. The connection to MongoDB is handled using the
`pymongo` package.

Requires:
    - pymongo

Functions:
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

from pymongo import MongoClient, errors


# ---- CRUD Operations for Students ----

def create_student(student_id, name, email):
    """
    Insert a new student into the 'students' collection.

    :param student_id: Unique ID of the student.
    :type student_id: int
    :param name: Name of the student.
    :type name: str
    :param email: Email of the student.
    :type email: str
    :raises errors.DuplicateKeyError: If the student ID already exists.
    :raises errors.PyMongoError: For other MongoDB-related errors.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['school']
        students = db['students']

        student = {
            '_id': student_id,
            'name': name,
            'email': email
        }

        students.insert_one(student)
        client.close()

    except errors.DuplicateKeyError:
        print(f"Student with ID {student_id} already exists.")
    except errors.PyMongoError as e:
        print("Error while creating student:", e)


def read_student(student_id):
    """
    Fetch a student document by ID from the 'students' collection.

    :param student_id: The ID of the student to fetch.
    :type student_id: int
    :return: The student document or None if not found.
    :rtype: dict or None
    :raises errors.PyMongoError: For any MongoDB-related errors.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['school']
        students = db['students']

        student = students.find_one({'_id': student_id})
        client.close()
        return student

    except errors.PyMongoError as e:
        print("Error while reading student:", e)


def update_student(student_id, name, email):
    """
    Update an existing student document in the 'students' collection.

    :param student_id: The ID of the student to update.
    :type student_id: int
    :param name: Updated name of the student.
    :type name: str
    :param email: Updated email of the student.
    :type email: str
    :raises errors.PyMongoError: For any MongoDB-related errors.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['school']
        students = db['students']

        result = students.update_one({'_id': student_id}, {'$set': {'name': name, 'email': email}})
        if result.matched_count == 0:
            print(f"No student found with ID {student_id}.")
        client.close()

    except errors.PyMongoError as e:
        print("Error while updating student:", e)


def delete_student(student_id):
    """
    Delete a student document by ID from the 'students' collection.

    :param student_id: The ID of the student to delete.
    :type student_id: int
    :raises errors.PyMongoError: For any MongoDB-related errors.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['school']
        students = db['students']

        result = students.delete_one({'_id': student_id})
        if result.deleted_count == 0:
            print(f"No student found with ID {student_id}.")
        client.close()

    except errors.PyMongoError as e:
        print("Error while deleting student:", e)


# ---- CRUD Operations for Courses ----

def create_course(course_id, title, description):
    """
    Insert a new course into the 'courses' collection.

    :param course_id: Unique ID of the course.
    :type course_id: int
    :param title: Title of the course.
    :type title: str
    :param description: Description of the course.
    :type description: str
    :raises errors.DuplicateKeyError: If course ID already exists.
    :raises errors.PyMongoError: For other MongoDB-related errors.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['school']
        courses = db['courses']

        course = {
            '_id': course_id,
            'title': title,
            'description': description
        }

        courses.insert_one(course)
        client.close()

    except errors.DuplicateKeyError:
        print(f"Course with ID {course_id} already exists.")
    except errors.PyMongoError as e:
        print("Error while creating course:", e)


def read_course(course_id):
    """
    Fetch a course document by ID from the 'courses' collection.

    :param course_id: The ID of the course to fetch.
    :type course_id: int
    :return: The course document or None if not found.
    :rtype: dict or None
    :raises errors.PyMongoError: For any MongoDB-related errors.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['school']
        courses = db['courses']

        course = courses.find_one({'_id': course_id})
        client.close()
        return course

    except errors.PyMongoError as e:
        print("Error while reading course:", e)


def update_course(course_id, title, description):
    """
    Update an existing course document in the 'courses' collection.

    :param course_id: The ID of the course to update.
    :type course_id: int
    :param title: Updated title of the course.
    :type title: str
    :param description: Updated description of the course.
    :type description: str
    :raises errors.PyMongoError: For any MongoDB-related errors.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['school']
        courses = db['courses']

        result = courses.update_one({'_id': course_id}, {'$set': {'title': title, 'description': description}})
        if result.matched_count == 0:
            print(f"No course found with ID {course_id}.")
        client.close()

    except errors.PyMongoError as e:
        print("Error while updating course:", e)


def delete_course(course_id):
    """
    Delete a course document by ID from the 'courses' collection.

    :param course_id: The ID of the course to delete.
    :type course_id: int
    :raises errors.PyMongoError: For any MongoDB-related errors.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['school']
        courses = db['courses']

        result = courses.delete_one({'_id': course_id})
        if result.deleted_count == 0:
            print(f"No course found with ID {course_id}.")
        client.close()

    except errors.PyMongoError as e:
        print("Error while deleting course:", e)


# ---- CRUD Operations for Enrollments ----

def enroll_student(enrollment_id, student_id, course_id):
    """
    Enroll a student in a course by adding a document to the 'enrollments' collection.

    :param enrollment_id: Unique ID of the enrollment.
    :type enrollment_id: int
    :param student_id: The student's ID.
    :type student_id: int
    :param course_id: The course ID.
    :type course_id: int
    :raises errors.DuplicateKeyError: If enrollment ID already exists.
    :raises errors.PyMongoError: For other MongoDB-related errors.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['school']
        enrollments = db['enrollments']

        enrollment = {
            '_id': enrollment_id,
            'student_id': student_id,
            'course_id': course_id
        }

        enrollments.insert_one(enrollment)
        client.close()

    except errors.DuplicateKeyError:
        print(f"Enrollment with ID {enrollment_id} already exists.")
    except errors.PyMongoError as e:
        print("Error while enrolling student:", e)


def read_enrollment(enrollment_id):
    """
    Fetch an enrollment document by ID from the 'enrollments' collection.

    :param enrollment_id: The ID of the enrollment to fetch.
    :type enrollment_id: int
    :return: The enrollment document or None if not found.
    :rtype: dict or None
    :raises errors.PyMongoError: For any MongoDB-related errors.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['school']
        enrollments = db['enrollments']

        enrollment = enrollments.find_one({'_id': enrollment_id})
        client.close()
        return enrollment

    except errors.PyMongoError as e:
        print("Error while reading enrollment:", e)


def delete_enrollment(enrollment_id):
    """
    Delete an enrollment document by ID from the 'enrollments' collection.

    :param enrollment_id: The ID of the enrollment to delete.
    :type enrollment_id: int
    :raises errors.PyMongoError: For any MongoDB-related errors.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['school']
        enrollments = db['enrollments']

        result = enrollments.delete_one({'_id': enrollment_id})
        if result.deleted_count == 0:
            print(f"No enrollment found with ID {enrollment_id}.")
        client.close()

    except errors.PyMongoError as e:
        print("Error while deleting enrollment:", e)
