from django.db.models.signals import post_save
from django.dispatch import receiver
from blog.models import Comment
from utils.email import send_email


@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        post_author_profile = instance.post.user
        if post_author_profile.email:
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
