from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.managers import CustomUserManager


LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('ru', 'Russian'),
    ('ua', 'Ukrainian'),
]


class CommunicationMethod(models.TextChoices):
    EMAIL = 'Email', _("Email")
    TELEGRAM = 'Telegram', _("Telegram")


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    first_name = models.CharField(
        _('first name'),
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=False,
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Phone Number")
    )
    telegram_id = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Telegram ID")
    )
    avatar = models.ImageField(
        upload_to='user_avatars/',
        null=True,
        blank=True,
        verbose_name=_("User Avatar")
    )
    communication_method = models.CharField(
        max_length=20,
        choices=CommunicationMethod.choices,
        default=CommunicationMethod.EMAIL,
        verbose_name=_("Preferred Communication Method")
    )
    preferred_language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='ua',
        verbose_name=_("Preferred Language")
    )
    preferred_timezone = models.CharField(
        max_length=50,
        default='UTC',
        verbose_name=_("Preferred Timezone")
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
