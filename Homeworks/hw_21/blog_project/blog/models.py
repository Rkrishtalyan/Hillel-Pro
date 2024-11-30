# ---- Import Statements ----
from django.db import models
from django.core.mail import send_mail

from ums.models import UserProfile


# ---- Model Definitions ----

class Category(models.Model):
    """
    Represent a category for organizing posts.

    :var name: The name of the category.
    :type name: str
    :var description: A brief description of the category.
    :type description: str
    """

    name = models.CharField(max_length=120)
    description = models.TextField()

    def __str__(self):
        """
        Return the string representation of the category.

        :return: The category name.
        :rtype: str
        """
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Tag(models.Model):
    """
    Represent a tag for categorizing posts.

    :var name: The name of the tag.
    :type name: str
    """

    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        """
        Return the string representation of the tag.

        :return: The tag name.
        :rtype: str
        """
        return self.name


class Post(models.Model):
    """
    Represent a blog post.

    :var title: The title of the post.
    :type title: str
    :var body: The content of the post.
    :type body: str
    :var image: An optional image for the post.
    :type image: ImageField
    :var is_active: Whether the post is active.
    :type is_active: bool
    :var created_at: The datetime the post was created.
    :type created_at: datetime
    :var updated_at: The datetime the post was last updated.
    :type updated_at: datetime
    :var user: The user who created the post.
    :type user: UserProfile
    :var category: The category to which the post belongs.
    :type category: Category
    :var tag: Tags associated with the post.
    :type tag: ManyToManyField
    """

    title = models.CharField(max_length=120)
    body = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        """
        Return the string representation of the post.

        :return: The post title.
        :rtype: str
        """
        return self.title

    def short_description(self):
        """
        Return a truncated version of the post body.

        :return: The truncated post body.
        :rtype: str
        """
        if len(self.body) > 100:
            return self.body[:100] + "..."
        return self.body

    def send_creation_email(self):
        """
        Send an email notification upon post creation.

        :raises Exception: If the email fails to send.
        """
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
    """
    Represent a comment on a blog post.

    :var message: The content of the comment.
    :type message: str
    :var created_at: The datetime the comment was created.
    :type created_at: datetime
    :var user: The user who made the comment.
    :type user: UserProfile
    :var post: The post the comment is associated with.
    :type post: Post
    """

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def short_description(self):
        """
        Return a truncated version of the comment message.

        :return: The truncated comment message.
        :rtype: str
        """
        if len(self.message) > 50:
            return self.message[:50] + "..."
        return self.message

    def __str__(self):
        """
        Return the string representation of the comment.

        :return: A string combining the post title and the truncated comment message.
        :rtype: str
        """
        return f'{self.post.title}: {self.short_description()}...'

    @classmethod
    def count_comments_in_post(cls, post):
        """
        Count the number of comments associated with a specific post.

        :param post: The post to count comments for.
        :type post: Post
        :return: The number of comments for the post.
        :rtype: int
        """
        return cls.objects.filter(post=post).count()
