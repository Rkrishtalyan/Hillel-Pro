from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator


# ---- User Profile Model Definition ----
class UserProfile(models.Model):
    """
    Represent a user profile with additional user details.

    This model extends the default User model by providing fields for bio,
    birth date, location, and avatar.

    :var user: A one-to-one relationship with the User model.
    :type user: models.OneToOneField
    :var bio: A short biography of the user.
    :type bio: models.TextField
    :var birth_date: The birth date of the user.
    :type birth_date: models.DateField
    :var location: The location of the user.
    :type location: models.CharField
    :var avatar: The user's avatar image.
    :type avatar: models.ImageField
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(
        max_length=500,
        validators=[MaxLengthValidator(500)],
        blank=True
    )
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    def __str__(self):
        """
        Return the username of the associated user.

        :return: The username of the User instance.
        :rtype: str
        """
        return self.user.username
