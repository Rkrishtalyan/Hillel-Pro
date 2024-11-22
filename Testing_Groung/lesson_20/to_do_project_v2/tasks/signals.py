from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Task


@receiver(post_save, sender=Task)
def task_create_signal(sender, instance, created, **kwargs):
    if created:
        print(f'Task created: {instance.title}')
