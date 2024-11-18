"""
Command for populating the `Book` model with random data.

This script defines a custom Django management command to generate random `Book` entries.
It uses the Faker library to create realistic placeholder data and supports specifying the
number of books to generate via a command-line argument.

Classes:
    - Command: Implements the logic for generating random `Book` entries.

Dependencies:
    - Django's management base command framework.
    - Faker library for generating random data.
    - Django's `User` and `Book` models.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random

from ...models import Book


class Command(BaseCommand):
    help = "Fills Book with random data"

    def handle(self, *args, **options):
        """
        Handle the command execution to generate random books.

        Deletes existing `Book` entries and creates a specified number of new books with
        random data. Assigns the first user in the database to each book as the associated user.

        :param args: Positional arguments.
        :param options: Command options including the count of books to create.
        """
        # ---- Clear existing books ----
        Book.objects.all().delete()

        faker = Faker()
        genres = ["Drama", "Novel", "Comedy", "Poem", "Story"]
        count = options['count']
        self.stdout.write(f"Generating random data for {count} books")

        # ---- Create random books ----
        for _ in range(count):
            Book.objects.create(
                title=faker.catch_phrase(),
                author=faker.name(),
                genre=random.choice(genres),
                publication_year=faker.year(),
                created_at=faker.date(),
                user=User.objects.first(),
            )

        self.stdout.write(self.style.SUCCESS(f"{count} books were created successfully"))

    def add_arguments(self, parser):
        """
        Add custom arguments for the management command.

        :param parser: Argument parser for the command.
        """
        parser.add_argument(
            '--count',
            type=int,
            help="Number of books to create",
            default=10
        )
