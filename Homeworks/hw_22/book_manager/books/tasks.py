import csv
import os
import codecs
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

from .models import Author, Book, Review


@shared_task
def import_books_from_csv(csv_file_path, user_email):
    """
    Import books, authors, and reviews from a CSV file and send a completion email.

    This task reads data from the provided CSV file to create or update
    `Author`, `Book`, and `Review` instances in the database. It also
    sends an email notification to the user upon completion and removes
    the CSV file from the filesystem.

    :param csv_file_path: The file path to the CSV file to import.
    :type csv_file_path: str
    :param user_email: The email address to notify upon task completion.
    :type user_email: str
    """
    # ---- Open and Parse CSV File ----
    with codecs.open(csv_file_path, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [field.strip() for field in reader.fieldnames]  # Normalize field names

        # ---- Process Each Row in CSV ----
        for row in reader:
            # Get or create the author
            author_name = row['author']
            author_date_of_birth = row['date_of_birth']
            author, created = Author.objects.get_or_create(
                name=author_name,
                date_of_birth=author_date_of_birth
            )

            # Get or create the book
            book_title = row['title']
            publication_date = row['publication_date']
            book, created = Book.objects.get_or_create(
                title=book_title,
                publication_date=publication_date
            )
            book.authors.add(author)  # Associate the author with the book

            # Create the review if review data is available
            reviewer_name = row.get('reviewer_name')
            rating = row.get('rating')
            comment = row.get('comment')
            if reviewer_name and rating and comment:
                Review.objects.create(
                    book=book,
                    reviewer_name=reviewer_name,
                    rating=int(rating),
                    comment=comment
                )

    # ---- Send Notification Email ----
    send_mail(
        'Book Import Completed',
        'Your book import task has been successfully completed.',
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

    # ---- Remove CSV File ----
    os.remove(csv_file_path)
