from django.db import models
from django.utils.translation import gettext_lazy as _

from pets.models._base_model import BaseModel
from pets.models.pet import Pet


class WeightRecord(BaseModel):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='weight_records',
        verbose_name=_("Pet")
    )
    date = models.DateField(verbose_name=_("Date"))
    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_("Weight (kg)")
    )

    def __str__(self):
        return f"{self.pet.name} - {self.date}: {self.weight_kg} kg"

    class Meta:
        verbose_name = _("Weight Record")
        verbose_name_plural = _("Weight Records")
