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
