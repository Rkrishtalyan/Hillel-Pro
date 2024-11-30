# ---- Import Statements ----
from django.db.models.signals import post_save
from django.dispatch import receiver

from blog.models import Comment
from utils.email import send_email


# ---- Signal Handlers ----

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    """
    Send a notification email to the post author when a new comment is created.

    :param sender: The model class that triggered the signal.
    :type sender: type
    :param instance: The instance of the model that triggered the signal.
    :type instance: Comment
    :param created: Indicates whether the instance was created.
    :type created: bool
    :param kwargs: Additional keyword arguments.
    """
    if created:
        # Get the post author's profile
        post_author_profile = instance.post.user
        if post_author_profile.email:
            # Send email notification
            send_email(
                subject='New Comment on Your Post',
                template_name='emails/comment_notification.html',
                context={
                    'username': post_author_profile.username,
                    'post_title': instance.post.title,
                    'post_url': f'/post/{instance.post.id}/',
                },
                recipient_list=[post_author_profile.email],
            )
