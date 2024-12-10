"""
Signals for the web_site app.

This module defines custom Django signals and their receivers for handling
specific model events.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from web_site.models import Article


# Task 8

article_raw_updated = Signal()


@receiver(post_save, sender=Article)
def mark_article_reviewed(sender, instance, **kwargs):
    """
    Automatically mark an article as reviewed if its body contains the word 'URGENT'.

    Triggered by the post_save signal of the Article model. If the article's body
    contains 'URGENT' and the article is not already reviewed, this function
    updates the reviewed status and saves the instance.

    :param sender: The model class that triggered the signal.
    :type sender: Model
    :param instance: The instance of the model that was saved.
    :type instance: Article
    :param kwargs: Additional keyword arguments.
    :type kwargs: dict
    """
    if 'URGENT' in instance.body and not instance.reviewed:
        instance.reviewed = True
        instance.save()
