from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from pets.models._base_model import BaseModel
from pets.models.pet import Pet
from pets.models.task import Task


class Vaccination(BaseModel):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='vaccination',
        verbose_name=_("Pet")
    )
    vaccine_name = models.CharField(
        max_length=200,
        verbose_name=_("Vaccine Name")
    )
    date_administered = models.DateField(
        verbose_name=_("Date Administered"),
        default=timezone.now
    )
    next_due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Next Due Date")
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes")
    )

    related_task = models.ForeignKey(
        Task,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='vaccination',
        verbose_name=_("Related Task")
    )

    def __str__(self):
        return f"{self.pet.name} - {self.vaccine_name}"

    class Meta:
        verbose_name = _("Vaccination")
        verbose_name_plural = _("Vaccinations")
