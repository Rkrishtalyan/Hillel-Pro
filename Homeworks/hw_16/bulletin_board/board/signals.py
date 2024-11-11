"""
Module for signal handling in the board app.

This module defines signal handlers that automatically trigger specific actions
after certain events in the `Ad` model. The signal handlers utilize Django’s
`post_save` signal to perform tasks immediately after an `Ad` instance is created.

Functions:
    - schedule_ad_deactivation: Schedules a background task to deactivate an ad after a set period.
    - send_notification: Sends a notification email to the user when an ad is created.
"""

# ---- Imports ----
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Ad
from .tasks import deactivate_ad_task


# ---- Signal Handlers ----

@receiver(post_save, sender=Ad)
def schedule_ad_deactivation(sender, instance, created, **kwargs):
    """
    Schedule a task to deactivate the ad after a certain period.

    :param sender: The model class sending the signal.
    :type sender: type
    :param instance: The specific Ad instance being saved.
    :type instance: Ad
    :param created: Boolean indicating if the instance was created.
    :type created: bool
    :param kwargs: Additional keyword arguments.
    :type kwargs: dict
    """
    if created:
        deactivate_ad_task(instance.id)


@receiver(post_save, sender=Ad)
def send_notification(sender, instance, created, **kwargs):
    """
    Send a notification email when an Ad instance is created.

    :param sender: The model class sending the signal.
    :type sender: type
    :param instance: The specific Ad instance being saved.
    :type instance: Ad
    :param created: Boolean indicating if the instance was created.
    :type created: bool
    :param kwargs: Additional keyword arguments.
    :type kwargs: dict
    """
    if created:
        instance.send_creation_email()
