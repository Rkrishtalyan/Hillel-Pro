from django.db import models


# ---- Author Model ----
class Author(models.Model):
    """
    Represent an author of books.

    Attributes:
        name (str): The full name of the author.
        date_of_birth (date): The author's date of birth.
    """
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    def __str__(self):
        """
        Return a string representation of the Author instance.

        :return: The name of the author.
        """
        return self.name


# ---- Book Model ----
class Book(models.Model):
    """
    Represent a book written by one or more authors.

    Attributes:
        title (str): The title of the book.
        authors (ManyToManyField): The authors who wrote the book.
        publication_date (date): The book's publication date.
    """
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name='books')
    publication_date = models.DateField()

    def __str__(self):
        """
        Return a string representation of the Book instance.

        :return: The title of the book.
        """
        return self.title


# ---- Review Model ----
class Review(models.Model):
    """
    Represent a review of a book.

    Attributes:
        book (ForeignKey): The book being reviewed.
        reviewer_name (str): The name of the reviewer.
        rating (int): The reviewer's rating of the book.
        comment (str): The reviewer's comments.
        created_at (datetime): The date and time when the review was created.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField(db_index=True)  # Indexed for fast lookups
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the Review instance.

        :return: A formatted string describing the review.
        """
        return f'Review of "{self.book.title}" by {self.reviewer_name}'
