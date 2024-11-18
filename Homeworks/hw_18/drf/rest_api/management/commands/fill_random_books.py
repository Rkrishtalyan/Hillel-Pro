from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
import random

from ...models import Book


class Command(BaseCommand):

    help = "Fills Book with random data"

    def handle(self, *args, **options):
        Book.objects.all().delete()

        faker = Faker()
        genres = ["Drama", "Novel", "Comedy", "Poem", "Story"]
        count = options['count']
        self.stdout.write(f"Generating random data for {count} books")

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
        parser.add_argument(
            '--count',
            type=int,
            help="Number of books to create",
            default=10
        )
