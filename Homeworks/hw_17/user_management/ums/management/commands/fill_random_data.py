from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

from ...models import UserProfile


# ---- Management Command for Filling UserProfiles with Random Data ----
class Command(BaseCommand):
    """
    Fill UserProfiles with randomly generated data using Faker.

    This management command deletes all existing UserProfiles and generates
    new users with associated profiles.

    :var help: A string describing the purpose of the command.
    :type help: str
    """

    help = "Fills UserProfiles with random data"

    def handle(self, *args, **options):
        """
        Handle the command execution logic.

        Deletes all existing UserProfiles and generates new users with random data.

        :param args: Additional positional arguments.
        :param options: Options passed to the command.
        """
        # ---- Clear Existing UserProfiles ----
        UserProfile.objects.all().delete()

        faker = Faker()
        count = options['count']
        self.stdout.write(f"Generating random data for {count} users")

        # ---- Generate Random Users and UserProfiles ----
        for _ in range(count):
            user = User.objects.create_user(
                username=faker.user_name(),
                email=faker.email(),
                password="password123"
            )

            UserProfile.objects.create(
                user=user,
                bio=faker.text(max_nb_chars=100),
                birth_date=faker.date_of_birth(minimum_age=18, maximum_age=80),
                location=faker.city()
            )

        self.stdout.write(self.style.SUCCESS(f"{count} users were created successfully"))

    def add_arguments(self, parser):
        """
        Add custom arguments to the command parser.

        :param parser: The command argument parser.
        :type parser: argparse.ArgumentParser
        """
        parser.add_argument(
            '--count',
            type=int,
            help="Number of users to create",
            default=10
        )
