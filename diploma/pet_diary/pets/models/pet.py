from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from pets.models._base_model import BaseModel


class Pet(BaseModel):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pets',
        verbose_name=_("Owner")
    )
    caregiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='caring_pets',
        verbose_name=_("Caregiver")
    )

    name = models.CharField(max_length=100, verbose_name=_("Pet Name"))
    species = models.CharField(max_length=100, verbose_name=_("Species"))
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("Birth Date"))
    breed = models.CharField(max_length=100, blank=True, verbose_name=_("Breed"))
    chip_number = models.CharField(max_length=50, blank=True, verbose_name=_("Chip Number"))
    avatar = models.ImageField(upload_to='pet_avatars/', null=True, blank=True, verbose_name=_("Avatar"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    confirmed_diagnoses = models.TextField(
        blank=True,
        verbose_name=_("Confirmed Diagnoses")
    )
    current_prescriptions = models.TextField(
        blank=True,
        verbose_name=_("Current Prescriptions")
    )
    ration = models.TextField(
        blank=True,
        verbose_name=_("Ration")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Pet")
        verbose_name_plural = _("Pets")
