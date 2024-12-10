from django.db import models
from django.contrib.auth.models import AbstractUser

from web_site.model_fields import PhoneNumberField


# Task 10

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"


# Task 1

class UpperCaseCharField(models.CharField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value:
            return value.upper()
        return value


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('lifestyle', 'Lifestyle'),
        ('news', 'News'),
        ('other', 'Other'),
    ]

    title = UpperCaseCharField(max_length=255)
    body = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    reviewed = models.BooleanField(default=False)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles')

    def count_words_in_title(self):
        return len(self.title.split())

    def __str__(self):
        return self.title


# Task 3

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.article.title}: {self.text[:30]}"


# Task 6

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=13, blank=True, null=True, unique=True)

    def __str__(self):
        return self.username


# Task 9

class SiteMetric(models.Model):
    request_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Total Requests: {self.request_count}"
