from django.contrib.auth.management.commands.createsuperuser import Command as SuperUserCommand
from django.core.management.base import CommandError
from ums.models import UserProfile

class Command(SuperUserCommand):
    def handle(self, *args, **options):
        super().handle(*args, **options)
        username = options.get('username')
        email = options.get('email')

        from django.contrib.auth.models import User
        try:
            superuser = User.objects.get(username=username)
            if not hasattr(superuser, 'userprofile'):
                UserProfile.objects.create(user=superuser, bio='Superuser account', location='Default Location')
                self.stdout.write(self.style.SUCCESS(f"UserProfile created for superuser '{username}'"))
        except User.DoesNotExist:
            raise CommandError(f"Superuser with username '{username}' not found.")
