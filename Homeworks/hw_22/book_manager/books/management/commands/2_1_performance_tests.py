from django.core.management.base import BaseCommand
from books.models import Book, Review
import time
from django.db import connection, reset_queries


class Command(BaseCommand):
    """
    Execute performance tests to compare queries with and without optimization.

    The command runs tests for three types of database relationships:
    One-to-Many, Many-to-Many, and ForeignKey relationships. Each test measures
    the execution time and the number of queries performed.
    """
    help = 'Run performance tests comparing queries with and without optimization.'

    def handle(self, *args, **options):
        """
        Execute all performance tests and display results in the console.

        The method performs multiple tests using Django's ORM with and without
        query optimization techniques (e.g., `prefetch_related`, `select_related`).
        """
        results = {}

        # ---- One To Many tests ----
        self.stdout.write("\nOne To Many tests")

        # Test 1: Books and Reviews without optimization
        reset_queries()
        start_time = time.time()
        books = Book.objects.all()
        for book in books:
            reviews = book.reviews.all()
            for review in reviews:
                a = review.rating  # Simulate processing
        elapsed_time = time.time() - start_time
        num_queries = len(connection.queries)
        results['test 1'] = {'time': elapsed_time, 'num_queries': num_queries}
        self.stdout.write(f"Test 1: Books and Reviews without optimization")
        self.stdout.write(f"Time taken: {results['test 1']['time']:.4f} seconds, Number of queries: {results['test 1']['num_queries']}")

        # Test 2: Books and Reviews with prefetch_related
        reset_queries()
        start_time = time.time()
        books = Book.objects.prefetch_related('reviews').all()
        for book in books:
            reviews = book.reviews.all()
            for review in reviews:
                a = review.rating  # Simulate processing
        elapsed_time = time.time() - start_time
        num_queries = len(connection.queries)
        results['test 2'] = {'time': elapsed_time, 'num_queries': num_queries}
        self.stdout.write(f"Test 2: Books and Reviews with prefetch_related")
        self.stdout.write(f"Time taken: {results['test 2']['time']:.4f} seconds, Number of queries: {results['test 2']['num_queries']}")

        # ---- Many To Many tests ----
        self.stdout.write("\nMany To Many tests")

        # Test 3: Books and Authors without optimization
        reset_queries()
        start_time = time.time()
        books = Book.objects.all()
        for book in books:
            authors = book.authors.all()
            for author in authors:
                a = author.name  # Simulate processing
        elapsed_time = time.time() - start_time
        num_queries = len(connection.queries)
        results['test 3'] = {'time': elapsed_time, 'num_queries': num_queries}
        self.stdout.write(f"Test 3: Books and Authors without optimization")
        self.stdout.write(f"Time taken: {results['test 3']['time']:.4f} seconds, Number of queries: {results['test 3']['num_queries']}")

        # Test 4: Books and Authors with prefetch_related
        reset_queries()
        start_time = time.time()
        books = Book.objects.prefetch_related('authors').all()
        for book in books:
            authors = book.authors.all()
            for author in authors:
                a = author.name  # Simulate processing
        elapsed_time = time.time() - start_time
        num_queries = len(connection.queries)
        results['test 4'] = {'time': elapsed_time, 'num_queries': num_queries}
        self.stdout.write(f"Test 4: Books and Authors with prefetch_related")
        self.stdout.write(f"Time taken: {results['test 4']['time']:.4f} seconds, Number of queries: {results['test 4']['num_queries']}")

        # ---- ForeignKey tests ----
        self.stdout.write("\nForeignKey tests")

        # Test 5: Reviews and Books without optimization
        reset_queries()
        start_time = time.time()
        reviews = Review.objects.all()
        for review in reviews:
            book = review.book
            a = book.title  # Simulate processing
        elapsed_time = time.time() - start_time
        num_queries = len(connection.queries)
        results['test 5'] = {'time': elapsed_time, 'num_queries': num_queries}
        self.stdout.write(f"Test 5: Reviews and Books without optimization")
        self.stdout.write(f"Time taken: {results['test 5']['time']:.4f} seconds, Number of queries: {results['test 5']['num_queries']}")

        # Test 6: Reviews and Books with select_related
        reset_queries()
        start_time = time.time()
        reviews = Review.objects.select_related('book').all()
        for review in reviews:
            book = review.book
            a = book.title  # Simulate processing
        elapsed_time = time.time() - start_time
        num_queries = len(connection.queries)
        results['test 6'] = {'time': elapsed_time, 'num_queries': num_queries}
        self.stdout.write(f"Test 6: Reviews and Books with select_related")
        self.stdout.write(f"Time taken: {results['test 6']['time']:.4f} seconds, Number of queries: {results['test 6']['num_queries']}")
