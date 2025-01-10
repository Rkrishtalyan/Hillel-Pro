from django.db.models.signals import post_save
from django.dispatch import receiver
from pets.models import VaccinationLog, Task
from django.utils.translation import gettext_lazy as _


@receiver(post_save, sender=VaccinationLog)
def create_vaccination_task(sender, instance, created, **kwargs):
    if created and instance.next_due_date:
        Task.objects.create(
            pet=instance.pet,
            title=_("Vaccination: ") + instance.vaccine_name,
            due_date=instance.next_due_date
        )
