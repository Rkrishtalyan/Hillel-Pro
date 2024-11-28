from django.core.management.base import BaseCommand
from faker import Faker

from ...models import UserProfile


# ---- Management Command for Filling UserProfiles with Random Data ----
class Command(BaseCommand):

    help = "Fills UserProfiles with random data"

    def handle(self, *args, **options):
        # ---- Clear Existing UserProfiles ----
        UserProfile.objects.all().delete()

        faker = Faker()
        count = options['count']
        self.stdout.write(f"Generating random data for {count} users")

        # ---- Generate Random Users and UserProfiles ----
        for _ in range(count):
            UserProfile.objects.create(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                bio=faker.text(max_nb_chars=100)
            )

        self.stdout.write(self.style.SUCCESS(f"{count} users were created successfully"))

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            help="Number of users to create",
            default=10
        )
