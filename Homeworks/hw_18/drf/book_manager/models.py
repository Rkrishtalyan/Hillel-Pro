"""
Define the application's database models.

This module contains the definition of the `Book` model, representing a book entity
with attributes such as title, author, genre, publication year, and the user who created it.

Classes:
    - Book: Represents a book with details and its association with a user.

Dependencies:
    - Django's ORM and `User` model for user associations.
"""

from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    """
    Represent a book entity.

    The `Book` model stores information about books including their title, author,
    genre, publication year, creation date, and the user associated with the book.

    :var title: The title of the book.
    :type title: str
    :var author: The author of the book.
    :type author: str
    :var genre: The genre of the book.
    :type genre: str
    :var publication_year: The year the book was published.
    :type publication_year: int
    :var created_at: The timestamp when the book was created.
    :type created_at: datetime
    :var user: The user associated with the book.
    :type user: User
    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        """
        Return a string representation of the book.

        :return: The title of the book.
        :rtype: str
        """
        return self.title
