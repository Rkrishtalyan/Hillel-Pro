from django.contrib.auth.models import User
from django.db import models
import random, string


def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


class URL(models.Model):
    original_url = models.URLField(unique=True)
    short_url = models.URLField(max_length=8, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = generate_short_url()
        super().save(*args, **kwargs)


class URLClick(models.Model):
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='clicks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.url} - {self.user} - {self.clicked_at}"



