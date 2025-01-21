from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
import uuid
import os


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at")
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET('User deleted'),
        related_name='%(app_label)s_%(class)s_created',
        verbose_name=_("Created by"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at")
    )
    edited_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_("Edited at")
    )
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_edited',
        verbose_name=_("Edited by")
    )
    deleted_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_("Deleted at")
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='%(app_label)s_%(class)s_deleted',
        verbose_name=_("Deleted by")
    )

    class Meta:
        abstract = True

    def mark_as_edited(self, user):
        self.edited_at = timezone.now()
        self.edited_by = user
        self.updated_by = user

    def mark_as_deleted(self, user):
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.updated_by = user


# -------------------------------
#       Pet model
# -------------------------------
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Pet")
        verbose_name_plural = _("Pets")


# -------------------------------
#       Image model
# -------------------------------
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


# -------------------------------
#       Weight Log model
# -------------------------------
class WeightLog(BaseModel):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='weight_logs',
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
        verbose_name = _("Weight Log")
        verbose_name_plural = _("Weight Logs")


# -------------------------------
#       PetDocument model
# -------------------------------
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


# -------------------------------
#       Task model
# -------------------------------
class Task(BaseModel):

    class TaskStatus(models.TextChoices):
        PLANNED = 'planned', _("Planned")
        OVERDUE = 'overdue', _("Overdue")
        DONE = 'done', _("Done")
        SKIPPED = 'skipped', _("Skipped")

    REMIND_BEFORE_CHOICES = [
        ('15_min', _("15 minutes")),
        ('1_hour', _("1 hour")),
        ('4_hours', _("4 hours")),
        ('12_hours', _("12 hours")),
        ('1_day', _("1 day")),
        ('3_days', _("3 days")),
        ('1_week', _("1 week")),
    ]

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_("Pet")
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_("Title")
    )
    due_datetime = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Due Date and Time")
    )
    remind_me = models.BooleanField(
        default=False,
        verbose_name=_("Remind Me")
    )
    remind_before = models.CharField(
        max_length=20,
        choices=REMIND_BEFORE_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Remind Before")
    )
    status = models.CharField(
        max_length=10,
        choices=TaskStatus.choices,
        default=TaskStatus.PLANNED,
        verbose_name=_("Status")
    )
    recurring = models.BooleanField(
        default=False,
        verbose_name=_("Recurring?")
    )
    recurring_days = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Number of days to repeat")
    )
    reminder_sent = models.BooleanField(
        default=False,
        verbose_name=_("Reminder Sent")
    )
    reminder_sent_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_("Reminder Sent at")
    )
    reminder_sent_with = models.CharField(
        max_length=20,
        blank=True,
    )

    skipped_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Skipped at"))
    skipped_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='skipped_tasks',
        verbose_name=_("Skipped By")
    )

    completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Completed at"))
    completed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='completed_tasks',
        verbose_name=_("Completed By")
    )

    # def mark_as_edited(self, user):
    #     super().mark_as_edited(user)

    # def mark_as_deleted(self, user):
    #     super().mark_as_deleted(user)

    def mark_as_skipped(self, user):
        self.status = self.TaskStatus.SKIPPED
        self.skipped_at = timezone.now()
        self.skipped_by = user

    def mark_as_done(self, user):
        self.status = self.TaskStatus.DONE
        self.completed_at = timezone.now()
        self.completed_by = user

    def mark_as_reminded_via_email(self):
        self.reminder_sent = True
        self.reminder_sent_at = timezone.now()
        self.reminder_sent_with = 'email'

    def mark_as_reminded_via_telegram(self):
        self.reminder_sent = True
        self.reminder_sent_at = timezone.now()
        self.reminder_sent_with = 'telegram'

    def __str__(self):
        return f"{self.title} (pet={self.pet.name}, status={self.status})"

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")


# -------------------------------
#     Vaccination Log model
# -------------------------------
class VaccinationLog(BaseModel):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='vaccination_logs',
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
        related_name='vaccination_log_record',
        verbose_name=_("Related Task")
    )

    def __str__(self):
        return f"{self.pet.name} - {self.vaccine_name}"

    class Meta:
        verbose_name = _("Vaccination Log")
        verbose_name_plural = _("Vaccination Logs")
