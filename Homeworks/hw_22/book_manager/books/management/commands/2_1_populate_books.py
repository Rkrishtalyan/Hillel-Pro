from django.core.management.base import BaseCommand
from faker import Faker
import random

from books.models import Author, Book, Review


class Command(BaseCommand):
    """
    Populate the database with fake authors, books, and reviews.

    This command generates a specified number of authors, books, and reviews
    using the Faker library and randomization. The generated data is stored
    in the database.
    """
    help = 'Populate the database with fake authors, books, and reviews.'

    def handle(self, *args, **options):
        """
        Create fake authors, books, and reviews and populate the database.

        This method generates:
        - 20 authors with random names and birthdates.
        - 50 books with random titles, publication dates, and authors.
        - 1–3 reviews per book with random reviewer names, ratings, and comments.

        :param args: Additional positional arguments (not used).
        :param options: Additional keyword arguments (not used).
        """
        fake = Faker()
        num_authors = 20  # Number of authors to create
        num_books = 50    # Number of books to create

        # ---- Create Authors ----
        authors = []
        for _ in range(num_authors):
            first_name = fake.first_name()
            last_name = fake.last_name()
            date_of_birth = fake.date_of_birth(minimum_age=25, maximum_age=80)
            author = Author.objects.create(
                name=f'{first_name} {last_name}',
                date_of_birth=date_of_birth
            )
            authors.append(author)

        # ---- Create Books ----
        books = []
        for _ in range(num_books):
            title = fake.catch_phrase()
            publication_date = fake.date_between(start_date='-10y', end_date='today')
            book = Book.objects.create(
                title=title,
                publication_date=publication_date
            )
            # Assign random authors to the book
            num_book_authors = random.randint(1, 2)
            book_authors = random.sample(authors, num_book_authors)
            book.authors.add(*book_authors)
            books.append(book)

        # ---- Create Reviews ----
        for book in books:
            num_reviews = random.randint(1, 3)
            for _ in range(num_reviews):
                reviewer_name = fake.first_name()
                rating = random.randint(1, 5)
                comment = fake.paragraph(nb_sentences=3)
                Review.objects.create(
                    book=book,
                    reviewer_name=reviewer_name,
                    rating=rating,
                    comment=comment
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database.'))
