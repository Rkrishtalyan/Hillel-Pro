from django.contrib.auth.models import User
from django.db import models
import random
import string


def generate_short_url():
    """
    Generate a random short URL string.

    The generated string consists of 8 random characters from ASCII letters and digits.

    :return: A randomly generated short URL string.
    :rtype: str
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


class URL(models.Model):
    """
    Represent a URL model with fields for original and shortened URLs.

    :var original_url: The original URL to be shortened.
    :type original_url: URLField
    :var short_url: The shortened URL string.
    :type short_url: URLField
    :var created_by: The user who created the URL.
    :type created_by: ForeignKey
    :var created_at: The timestamp when the URL was created.
    :type created_at: DateTimeField
    :var custom_name: An optional custom name for the shortened URL.
    :type custom_name: CharField
    """
    original_url = models.URLField(unique=True)
    short_url = models.URLField(max_length=8, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    custom_name = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Override the save method to auto-generate a short URL if not provided.

        :param args: Positional arguments for the save method.
        :param kwargs: Keyword arguments for the save method.
        """
        if not self.short_url:
            candidate = generate_short_url()
            while URL.objects.filter(short_url=candidate).exists():
                candidate = generate_short_url()
            self.short_url = candidate
        super().save(*args, **kwargs)


class URLClick(models.Model):
    """
    Represent a model for tracking URL clicks.

    :var url: The associated URL instance.
    :type url: ForeignKey
    :var user: The user who clicked the URL (optional).
    :type user: ForeignKey
    :var clicked_at: The timestamp of the click.
    :type clicked_at: DateTimeField
    :var device_type: The type of device used to click the URL.
    :type device_type: CharField
    :var country: The country from which the URL was clicked.
    :type country: CharField
    """
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='clicks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)
    device_type = models.CharField(max_length=50, default='Unknown')
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        """
        Return a string representation of the URLClick instance.

        :return: A string combining the URL, user, and click timestamp.
        :rtype: str
        """
        return f"{self.url} - {self.user} - {self.clicked_at}"
