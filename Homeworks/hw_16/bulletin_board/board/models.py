# ---- Imports ----
from datetime import timedelta
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

# ---- Models ----

class UserProfile(models.Model):
    """
    Represent a user profile with additional information like phone number and address.

    :var user: Reference to the Django User model.
    :type user: models.OneToOneField
    :var phone_number: The user's phone number, must be unique.
    :type phone_number: str
    :var address: The user's address.
    :type address: str
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, unique=True)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def username(self):
        """Return the username of the associated User."""
        return self.user.username

    @property
    def first_name(self):
        """Return the first name of the associated User."""
        return self.user.first_name

    @property
    def last_name(self):
        """Return the last name of the associated User."""
        return self.user.last_name


class Category(models.Model):
    """
    Represent an ad category.

    :var name: The name of the category, must be unique.
    :type name: str
    :var description: A description of the category.
    :type description: str
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    def count_active_ads(self):
        """Return the count of active ads in this category."""
        return self.ad_set.filter(is_active=True).count()

    count_active_ads.short_description = 'Active ads'

    class Meta:
        verbose_name_plural = 'Categories'


class Ad(models.Model):
    """
    Represent an advertisement with title, description, and other metadata.

    :var title: The title of the ad, must be unique.
    :type title: str
    :var description: The ad's description.
    :type description: str
    :var price: The price of the ad, minimum value enforced.
    :type price: Decimal
    :var created_at: Timestamp for ad creation.
    :type created_at: DateTime
    :var updated_at: Timestamp for ad updates.
    :type updated_at: DateTime
    :var is_active: Whether the ad is active.
    :type is_active: bool
    :var user: The UserProfile associated with the ad.
    :type user: UserProfile
    :var category: The categories associated with the ad.
    :type category: Category
    """
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    def short_description(self):
        """Return a shortened version of the description if it exceeds 100 characters."""
        if len(self.description) > 100:
            return self.description[:100] + "..."
        return self.description

    @classmethod
    def deactivate_ad(cls):
        """
        Deactivate ads older than 30 days.

        :return: None
        """
        expiration_date = timezone.now() - timedelta(days=30)
        expired_ads = cls.objects.filter(is_active=True, created_at__lte=expiration_date)
        expired_ads.update(is_active=False)

    def send_creation_email(self):
        """
        Send a creation confirmation email to the user.

        :return: None
        :raises Exception: If the email fails to send.
        """
        user_email = self.user.user.email
        ad_title = self.title
        recipient_name = self.user.first_name or self.user.username

        try:
            send_mail(
                subject='Your Ad has been created',
                message=(
                    f'Dear {recipient_name},\n\n'
                    f'Your ad "{ad_title}" has been successfully created.\n\n'
                    'Thank you for using our service!'
                ),
                from_email='no-reply@yourdomain.com',
                recipient_list=[user_email],
                fail_silently=False,
            )
        except Exception as e:
            print(f'Failed to send email to {user_email}: {e}')
            raise e


class Comment(models.Model):
    """
    Represent a comment on an ad with content, creation timestamp, and references to the ad and user.

    :var content: The content of the comment.
    :type content: str
    :var created_at: Timestamp for comment creation.
    :type created_at: DateTime
    :var ad: The ad the comment is associated with.
    :type ad: Ad
    :var user: The user who posted the comment.
    :type user: UserProfile
    """
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ad.title}: {self.short_description()}..."

    def short_description(self):
        """Return a shortened version of the content if it exceeds 50 characters."""
        if len(self.content) > 50:
            return self.content[:50] + '...'
        return self.content

    @classmethod
    def comments_in_ad(cls, ad):
        """Return the count of comments associated with a specific ad."""
        return cls.objects.filter(ad=ad).count()
