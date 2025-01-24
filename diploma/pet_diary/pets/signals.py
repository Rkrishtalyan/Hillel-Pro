from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from pets.models import Vaccination, Task
from pets.notifications import _notify_owner_about_result


@receiver(post_save, sender=Vaccination)
def create_vaccination_task(sender, instance, created, **kwargs):
    if created and instance.next_due_date:
        task = Task.objects.create(
            pet=instance.pet,
            created_by=instance.created_by,
            title=_("Vaccination: ") + instance.vaccine_name,
            due_datetime=instance.next_due_date,
            remind_me = True,
            remind_before='1_day',
        )
        vaccination = Vaccination.objects.filter(
            id=instance.id,
        )
        vaccination.update(related_task_id=task.id)


@receiver(post_save, sender=Vaccination)
def update_vaccination_task(sender, instance, created, **kwargs):
    if created:
        return

    if not instance.related_task_id:
        create_vaccination_task(sender, instance, created, **kwargs)

    try:
        task = Task.objects.get(id=instance.related_task_id)
    except ObjectDoesNotExist:
        return

    if instance.next_due_date and task.due_datetime.date() != instance.next_due_date:
        task.due_datetime = instance.next_due_date
        task.reminder_sent = False
        task.save()


@receiver(post_save, sender=Vaccination)
def delete_vaccination_task(sender, instance, created, **kwargs):
    if created:
        return

    if not instance.related_task_id:
        return

    try:
        task = Task.objects.get(id=instance.related_task_id)
    except ObjectDoesNotExist:
        return

    if instance.deleted_at or not instance.due_datetime:
        task.mark_as_deleted(instance.deleted_by)
        task.save()


@receiver(post_save, sender=Task)
def notify_task_owner_if_caretaker_completed(sender, instance, created, **kwargs):
    if created:
        return

    caretaker = instance.pet.caregiver
    if not caretaker:
        return

    if instance.status == Task.TaskStatus.DONE and instance.completed_by == caretaker:
        _notify_owner_about_result(instance, Task.TaskStatus.DONE)
    elif instance.status == Task.TaskStatus.SKIPPED and instance.skipped_by == caretaker:
        _notify_owner_about_result(instance, Task.TaskStatus.SKIPPED)
