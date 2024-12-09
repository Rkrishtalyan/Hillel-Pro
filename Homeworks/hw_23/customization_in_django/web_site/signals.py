from django.db.models.signals import post_save
from django.dispatch import receiver
from django.dispatch import Signal

from web_site.models import Article


# Task 8

article_raw_updated = Signal()


@receiver(post_save, sender=Article)
def mark_article_reviewed(sender, instance, **kwargs):
    if 'URGENT' in instance.body and not instance.reviewed:
        instance.reviewed = True
        instance.save()
