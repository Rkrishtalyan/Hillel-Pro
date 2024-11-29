from django.db import models
from django.core.mail import send_mail

from ums.models import UserProfile


class Category(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=120)
    body = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def short_description(self):
        if len(self.body) > 100:
            return self.body[:100] + "..."
        return self.body

    def send_creation_email(self):
        user_email = self.user.user.email
        post_title = self.title
        recipient_name = self.user.first_name or self.user.username

        try:
            send_mail(
                subject='Your post has been created',
                message=(
                    f'Dear {recipient_name},\n\n'
                    f'Your post "{post_title}" has been successfully created.\n\n'
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
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def short_description(self):
        if len(self.message) > 50:
            return self.message[:50] + "..."
        return self.message

    def __str__(self):
        return f'{self.post.title}: {self.short_description()}...'

    @classmethod
    def count_comments_in_post(cls, post):
        return cls.objects.filter(post=post).count()