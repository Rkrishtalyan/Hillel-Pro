# ---- Import Statements ----
from django.db import models
from django.contrib.auth.models import User


# ---- Model Definitions ----

class UserProfile(models.Model):
    """
    Represent a user's profile with extended information.

    :var user: The associated User model.
    :type user: User
    :var first_name: The user's first name.
    :type first_name: str
    :var last_name: The user's last name.
    :type last_name: str
    :var email: The user's email address.
    :type email: str
    :var bio: A brief biography of the user.
    :type bio: str
    :var birth_date: The user's birth date.
    :type birth_date: datetime.date
    :var location: The user's location.
    :type location: str
    :var avatar: The user's profile picture.
    :type avatar: ImageField
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    @property
    def username(self):
        """
        Return the username of the associated user.

        :return: The username of the user.
        :rtype: str
        """
        return self.user.username

    # @property
    # def first_name(self):
    #     return self.user.first_name
    #
    # @property
    # def last_name(self):
    #     return self.user.last_name

    def __str__(self):
        """
        Return the string representation of the UserProfile.

        :return: The username of the associated user.
        :rtype: str
        """
        return self.user.username
