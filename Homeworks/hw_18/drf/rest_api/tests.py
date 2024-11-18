"""
Automated tests for the Book API.

This module contains test cases to validate the behavior of the Book API, including CRUD operations and permission checks.
The tests cover authenticated and unauthenticated access scenarios for various user roles (superuser, staff user, regular user).

Classes:
    - BookAPITestCase: Tests for the Book API endpoints.

Dependencies:
    - Django REST framework's APITestCase for testing APIs.
    - Django's URL resolver for generating endpoint URLs.
    - Django's User model for creating test users.
    - Book model for creating and validating test data.
"""
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book


class BookAPITestCase(APITestCase):
    """
    Test suite for the Book API.

    This test case includes tests for listing, creating, and deleting books,
    as well as validating permissions for different user roles.
    """
    def setUp(self):
        """
        Set up test data and users for the test suite.

        Creates a superuser, a staff user, and a regular user. Also, populates
        the database with two books associated with different users.
        """
        self.superuser = User.objects.create_superuser(username='ruslank', password='SuperPass123')
        self.staff_user = User.objects.create_user(username='staff_user', password='StaffPass123', is_staff=True)
        self.regular_user = User.objects.create_user(username='test_user', password='TestPass123')

        Book.objects.create(title='Book 1', author='Author A', genre='Fiction', publication_year=2020,
                            user=self.regular_user)
        Book.objects.create(title='Book 2', author='Author B', genre='Non-Fiction', publication_year=2021,
                            user=self.staff_user)

    def test_list_books_authenticated(self):
        """
        Test authenticated users can list books.

        Logs in as a regular user and ensures the user can retrieve the list
        of books and that the expected number of results is returned.
        """
        self.client.login(username='test_user', password='TestPass123')

        url = reverse('book-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_book_authenticated(self):
        """
        Test authenticated users can create books.

        Logs in as a regular user and attempts to create a book. Verifies the book
        is successfully created with the expected attributes.
        """
        self.client.login(username='test_user', password='TestPass123')

        url = reverse('book-list')
        data = {
            "title": "New Book",
            "author": "Author C",
            "genre": "Science Fiction",
            "publication_year": 2022
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Book")
        self.assertEqual(response.data['user'], 'test_user')

    def test_delete_book_regular_user_forbidden(self):
        """
        Test regular users cannot delete books they do not own.

        Logs in as a regular user and attempts to delete a book. Ensures the
        deletion is forbidden and the book remains in the database.
        """
        self.client.login(username='test_user', password='TestPass123')

        book = Book.objects.first()
        url = reverse('book-detail', args=[book.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_superuser(self):
        """
        Test superusers can delete any book.

        Logs in as a superuser and deletes a book. Verifies the book is removed
        from the database.
        """
        self.client.login(username='ruslank', password='SuperPass123')

        book = Book.objects.first()
        url = reverse('book-detail', args=[book.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=book.id).exists())

    def test_access_books_unauthenticated(self):
        """
        Test unauthenticated users cannot access the book list.

        Attempts to retrieve the list of books without logging in. Ensures
        the response status is unauthorized.
        """
        url = reverse('book-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
