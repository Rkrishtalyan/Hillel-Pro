import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from pets.models._base_model import BaseModel
from pets.models.pet import Pet


def pet_image_upload_to(instance, filename):
    return os.path.join('pet_images', str(instance.pet.id), filename)


class PetImage(BaseModel):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_("Pet")
    )
    path = models.ImageField(
        upload_to=pet_image_upload_to,
        verbose_name=_("Image")
    )
    image_name = models.CharField(
        max_length=100,
        verbose_name=_("Image Name")
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Uploaded at")
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes")
    )

    def __str__(self):
        return f"{self.pet.name} (id={self.id})"

    class Meta:
        verbose_name = _("Pet Image")
        verbose_name_plural = _("Pet Images")
