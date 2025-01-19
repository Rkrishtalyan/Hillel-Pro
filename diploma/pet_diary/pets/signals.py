from django.db.models.signals import post_save
from django.dispatch import receiver
from pets.models import VaccinationLog, Task
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from pets.notifications import _notify_owner_about_result


@receiver(post_save, sender=VaccinationLog)
def create_vaccination_task(sender, instance, created, **kwargs):
    if created and instance.next_due_date:
        Task.objects.create(
            pet=instance.pet,
            title=_("Vaccination: ") + instance.vaccine_name,
            due_datetime=instance.next_due_date
        )

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
