from django.db import models

# Task 1

class UpperCaseCharField(models.CharField):
    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value:
            return value.upper()
        return value


class Article(models.Model):
    title = UpperCaseCharField(max_length=255)
    body = models.TextField()

    def count_words_in_title(self):
        return len(self.title.split())

    def __str__(self):
        return self.title
