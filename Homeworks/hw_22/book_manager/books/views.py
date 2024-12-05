import uuid
from django.core.exceptions import FieldError
from django.db.models import Avg, Count, F
from django.db.models.expressions import OrderBy
from django.db import connection
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.urls import reverse
from django.contrib import messages
from celery.result import AsyncResult
from django.views import View
from django.conf import settings

from .tasks import import_books_from_csv
from .models import Book, Author, Review


# ---- Book List Views ----
# @cache_page(60 * 15)  # Commented to fix MongoDB compatibility issues
def book_list(request):
    """
    Display a list of books with prefetching for authors.

    :param request: The HTTP request object.
    :return: Rendered template for the book list.
    """
    books = Book.objects.prefetch_related('authors').all()
    return render(request, 'books/book_list.html', {'books': books})


def unoptimized_book_list(request):
    """
    Display a list of books without any query optimizations.

    :param request: The HTTP request object.
    :return: Rendered template for the unoptimized book list.
    """
    books = Book.objects.all()
    return render(request, 'books/unoptimized_book_list.html', {'books': books})


def optimized_book_list(request):
    """
    Display a list of books with prefetching for authors and reviews.

    :param request: The HTTP request object.
    :return: Rendered template for the optimized book list.
    """
    books = Book.objects.prefetch_related('authors', 'reviews').all()
    return render(request, 'books/optimized_book_list.html', {'books': books})


# ---- File Upload and Task Handling ----
def upload_books_csv(request):
    """
    Handle CSV file upload and initiate an asynchronous import task.

    :param request: The HTTP request object.
    :return: Redirect to task status or rendered upload form.
    """
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        user_email = request.POST.get('email')

        temp_filename = f"{uuid.uuid4()}_{csv_file.name}"
        temp_filepath = settings.MEDIA_ROOT / temp_filename

        with open(temp_filepath, 'wb+') as destination:
            for chunk in csv_file.chunks():
                destination.write(chunk)

        task = import_books_from_csv.delay(str(temp_filepath), user_email)

        messages.success(request, f"Import started! Task ID: {task.id}")
        return redirect(reverse('task_status', args=[task.id]))

    return render(request, 'books/upload_csv.html')


def task_status(request, task_id):
    """
    Display the status of an asynchronous task.

    :param request: The HTTP request object.
    :param task_id: The ID of the task.
    :return: Rendered template with task status information.
    """
    result = AsyncResult(task_id)
    return render(request, 'books/task_status.html', {'task': result, 'task_id': task_id})


# Task 3.1
# ---- ORM Queries ----
def orm_queries(request):
    """
    Perform ORM queries for average ratings and review counts.

    :param request: The HTTP request object.
    :return: Rendered template with authors and books data.
    """
    authors = Author.objects.annotate(
        avg_books_rating=Avg('books__reviews__rating')
    ).order_by('name')

    books = Book.objects.annotate(
        rating_count=Count('reviews'),
        avg_book_rating=Avg('reviews__rating')
    ).order_by(
        OrderBy(F('rating_count'), descending=True),
        OrderBy(F('avg_book_rating'), descending=True)
    )

    return render(request, 'books/orm_queries.html', {'authors': authors, 'books': books})


# Task 3.2
# ---- Raw SQL Queries ----
class AuthorBookReviewView(View):
    """
    View to display authors with books having over 10 reviews using raw SQL.

    Features:
    - Retrieves distinct authors with at least one book having more than 10 reviews.
    - Gets the total count of books.
    """

    def get(self, request):
        """
        Handle GET requests to display authors and total books.

        :param request: The HTTP request object.
        :return: Rendered template with authors and book counts.
        """
        authors = self.get_authors_with_books_over_10_reviews()
        total_books = self.get_total_books_count()
        return render(request, 'books/raw_sql_queries.html',
                      {'authors': authors, 'total_books': total_books})

    def get_authors_with_books_over_10_reviews(self):
        """
        Fetch authors with books having more than 10 reviews using raw SQL.

        :return: List of authors with names.
        """
        with connection.cursor() as cursor:
            query = """
                SELECT DISTINCT a.name
                FROM books_author a
                JOIN books_book_authors ba ON a.id = ba.author_id
                JOIN books_book b ON ba.book_id = b.id
                JOIN books_review r ON b.id = r.book_id
                GROUP BY a.name
                HAVING COUNT(r.id) > %s;
            """
            params = [10]
            cursor.execute(query, params)
            rows = cursor.fetchall()

        authors = [{'name': row[0]} for row in rows]
        return authors

    def get_total_books_count(self):
        """
        Fetch the total count of books using raw SQL.

        :return: Total number of books.
        """
        with connection.cursor() as cursor:
            query = "SELECT COUNT(*) FROM books_book;"
            cursor.execute(query)
            row = cursor.fetchone()

        total_books = row[0] if row else 0
        return total_books


# Task 3.4
# ---- No SQL ORM Queries ----
def no_sql_orm_queries(request):
    """
    Handle ORM queries and fallback to empty results in case of errors.

    :param request: The HTTP request object.
    :return: Rendered template with authors and books data or empty results.
    """
    try:
        authors = Author.objects.annotate(
            avg_books_rating=Avg('books__reviews__rating')
        ).order_by('name')

        books = Book.objects.annotate(
            rating_count=Count('reviews'),
            avg_book_rating=Avg('reviews__rating')
        ).order_by(
            '-rating_count',
            '-avg_book_rating'
        )

    except FieldError:
        authors = Author.objects.none()
        books = Book.objects.none()

    return render(request, 'books/orm_queries.html', {'authors': authors, 'books': books})
