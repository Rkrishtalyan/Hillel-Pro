# ---- Django User Profile Model Definition ----

from django.db import models


class UserProfile(models.Model):
    """
    Represent a user profile with a first name, last name, and bio.

    This model stores basic user profile information and provides
    a string representation of the user.

    :var first_name: The first name of the user.
    :type first_name: str
    :var last_name: The last name of the user.
    :type last_name: str
    :var bio: A brief biography of the user.
    :type bio: str
    """

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.TextField()

    def __str__(self):
        """
        Return a string representation of the user's full name.

        :return: A string combining the first and last name.
        :rtype: str
        """
        return f'{self.first_name} {self.last_name}'
