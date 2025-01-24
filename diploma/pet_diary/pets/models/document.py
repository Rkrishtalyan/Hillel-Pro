import os

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from pets.models._base_model import BaseModel
from pets.models.pet import Pet


def pet_document_upload_to(instance, filename):
    return os.path.join('pet_documents', str(instance.pet.id), filename)


class PetDocument(BaseModel):
    class DocumentType(models.TextChoices):
        ANALYSIS = 'analysis', _("Analysis Result")
        EXAMINATION = 'examination', _("Examination Result")
        CONCLUSION = 'conclusion', _("Doctor Conclusion")
        OTHER = 'other', _("Other")

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_("Pet")
    )
    doc_file = models.FileField(
        upload_to=pet_document_upload_to,
        verbose_name=_("Document File")
    )
    doc_file_name = models.CharField(
        max_length=100,
        verbose_name=_("Document File Name")
    )
    doc_type = models.CharField(
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
        verbose_name=_("Document Type")
    )
    doc_date = models.DateField(
        default=timezone.now,
        verbose_name=_("Document Date")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )

    def __str__(self):
        return f"{self.get_doc_type_display()} ({self.pet.name})"

    class Meta:
        verbose_name = _("Pet Document")
        verbose_name_plural = _("Pet Documents")
        ordering = ['-doc_date', '-created_at']
