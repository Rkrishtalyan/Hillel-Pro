"""
Main script for demonstrating CRUD operations using SQLite and MongoDB.

This script performs a series of operations on both an SQLite database and a
MongoDB database. The operations include creating, reading, updating, and
deleting students, courses, and enrollments in both databases.

Modules used:
    - sqlite_db: Provides functions for CRUD operations on an SQLite database.
    - mongo_db: Provides functions for CRUD operations on a MongoDB database.

Operations:
    - Create, read, update, delete students.
    - Create, read, update, delete courses.
    - Enroll students in courses and manage enrollments.
"""

# ---- Imports ----
import sqlite_db as sqlite
import mongo_db as mongo

# ---- Create tables/collections ----
sqlite.create_tables()
mongo.create_collections()

# --- SQLite operations ---
print("\n--- SQLite Operations ---")

# Create student
sqlite.create_student(1, 'John Doe', 'john@example.com')

# Read student
student = sqlite.read_student(1)
print('\nSQLite Student:')
if student:
    for key, value in student.items():
        print(f'  {key}: {value}')
else:
    print('  Student not found.')

# Update student
sqlite.update_student(1, 'John Doe Jr.', 'johnjr@example.com')

# Read updated student
student = sqlite.read_student(1)
print('\nSQLite Updated Student:')
if student:
    for key, value in student.items():
        print(f'  {key}: {value}')
else:
    print('  Student not found.')

# Delete student
sqlite.delete_student(1)
print('SQLite Student deleted successfully.')

# Try to read deleted student
student = sqlite.read_student(1)
if not student:
    print('SQLite Student not found after deletion.')

# Create course
sqlite.create_course(1, 'Mathematics', 'An introduction to mathematics')

# Read course
course = sqlite.read_course(1)
print('\nSQLite Course:')
if course:
    for key, value in course.items():
        print(f'  {key}: {value}')
else:
    print('  Course not found.')

# Enroll student (creating new student)
sqlite.create_student(2, 'Alice Smith', 'alice@example.com')
student = sqlite.read_student(2)
print('\nSQLite Second Student:')
if student:
    for key, value in student.items():
        print(f'  {key}: {value}')
else:
    print('  Student not found.')

sqlite.enroll_student(1, 2, 1)
enrollment = sqlite.read_enrollment(1)
print('\nSQLite Enrollment:')
if enrollment:
    for key, value in enrollment.items():
        print(f'  {key}: {value}')
else:
    print('  Enrollment not found.')

# Delete enrollment
sqlite.delete_enrollment(1)
print('SQLite Enrollment deleted successfully.')

# Try to read deleted enrollment
enrollment = sqlite.read_enrollment(1)
if not enrollment:
    print('SQLite Enrollment not found after deletion.')


# --- MongoDB operations ---
print("\n\n--- MongoDB Operations ---")

# Create student
mongo.create_student(1, 'John Doe', 'john@example.com')
student = mongo.read_student(1)
print('\nMongoDB Student:')
if student:
    for key, value in student.items():
        print(f'  {key}: {value}')
else:
    print('  Student not found.')

# Update student
mongo.update_student(1, 'John Doe Jr.', 'johnjr@example.com')
student = mongo.read_student(1)
print('\nMongoDB Updated Student:')
if student:
    for key, value in student.items():
        print(f'  {key}: {value}')
else:
    print('  Student not found.')

# Delete student
mongo.delete_student(1)
print('MongoDB Student deleted successfully.')

# Try to read deleted student
student = mongo.read_student(1)
if not student:
    print('MongoDB Student not found after deletion.')

# Create course
mongo.create_course(1, 'Mathematics', 'An introduction to mathematics')
course = mongo.read_course(1)
print('\nMongoDB Course:')
if course:
    for key, value in course.items():
        print(f'  {key}: {value}')
else:
    print('  Course not found.')

# Enroll student (creating new student)
mongo.create_student(2, 'Alice Smith', 'alice@example.com')
student = mongo.read_student(2)
print('\nMongoDB Second Student:')
if student:
    for key, value in student.items():
        print(f'  {key}: {value}')
else:
    print('  Student not found.')

mongo.enroll_student(1, 2, 1)
enrollment = mongo.read_enrollment(1)
print('\nMongoDB Enrollment:')
if enrollment:
    for key, value in enrollment.items():
        print(f'  {key}: {value}')
else:
    print('  Enrollment not found.')

# Delete enrollment
mongo.delete_enrollment(1)
print('MongoDB Enrollment deleted successfully.')

# Try to read deleted enrollment
enrollment = mongo.read_enrollment(1)
if not enrollment:
    print('MongoDB Enrollment not found after deletion.')
