"""
Models for the web_site app.

This module defines custom models and fields used in the web_site application.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser

from web_site.model_fields import PhoneNumberField


# Task 10

class Contact(models.Model):
    """
    Represents a contact with a name and unique phone number.

    :var name: The name of the contact.
    :type name: str
    :var phone: The phone number of the contact, validated for format.
    :type phone: PhoneNumberField
    """
    name = models.CharField(max_length=100)
    phone = PhoneNumberField(unique=True)

    def __str__(self):
        """
        Return a string representation of the contact.

        :return: A string in the format "name (phone)".
        :rtype: str
        """
        return f"{self.name} ({self.phone})"


# Task 1

class UpperCaseCharField(models.CharField):
    """
    A custom CharField that converts all input values to uppercase when saving.
    """

    def get_prep_value(self, value):
        """
        Prepare the value for saving by converting it to uppercase.

        :param value: The input value to prepare.
        :type value: str
        :return: The value converted to uppercase, or None if the value is None.
        :rtype: str or None
        """
        value = super().get_prep_value(value)
        if value:
            return value.upper()
        return value


class Article(models.Model):
    """
    Represents an article with a title, body, category, and related contact.

    :var title: The title of the article, stored in uppercase.
    :type title: UpperCaseCharField
    :var body: The body content of the article.
    :type body: TextField
    :var category: The category of the article, chosen from predefined options.
    :type category: str
    :var reviewed: Indicates whether the article has been reviewed.
    :type reviewed: bool
    :var contact: The associated contact for the article, nullable and optional.
    :type contact: ForeignKey to Contact
    """
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
        """
        Count the number of words in the article title.

        :return: The number of words in the title.
        :rtype: int
        """
        return len(self.title.split())

    def __str__(self):
        """
        Return the title of the article as its string representation.

        :return: The article title.
        :rtype: str
        """
        return self.title


# Task 3

class Comment(models.Model):
    """
    Represents a comment on an article.

    :var article: The related article for this comment.
    :type article: ForeignKey to Article
    :var text: The content of the comment.
    :type text: TextField
    :var created_at: The timestamp when the comment was created.
    :type created_at: DateTimeField
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a truncated string representation of the comment.

        :return: A string in the format "Comment on article_title: text_excerpt".
        :rtype: str
        """
        return f"Comment on {self.article.title}: {self.text[:30]}"


# Task 6

class CustomUser(AbstractUser):
    """
    Represents a custom user model with an optional phone number field.

    :var phone_number: The user's phone number, optional and unique.
    :type phone_number: str
    """
    phone_number = models.CharField(max_length=13, blank=True, null=True, unique=True)

    def __str__(self):
        """
        Return the username as the string representation of the user.

        :return: The username of the user.
        :rtype: str
        """
        return self.username


# Task 9

class SiteMetric(models.Model):
    """
    Tracks site metrics such as the number of requests received.

    :var request_count: The total number of HTTP requests recorded.
    :type request_count: int
    """
    request_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        """
        Return a string representation of the total request count.

        :return: A string in the format "Total Requests: request_count".
        :rtype: str
        """
        return f"Total Requests: {self.request_count}"
